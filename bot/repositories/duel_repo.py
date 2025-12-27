from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.duel import Duel
from bot.models.duel_member import DuelMember


async def create_duel_steps(
    session: AsyncSession,
    chat_id: int,
    created_by: int,
    opponent_user_id: int,
    days: int = 7,
) -> Duel:
    now = datetime.now(timezone.utc)
    duel = Duel(
        chat_id=chat_id,
        created_by=created_by,
        metric="steps",
        start_at=now,
        end_at=now + timedelta(days=days),
        status="pending",
    )
    session.add(duel)
    await session.flush()  # گرفتن duel.id بدون commit

    # challenger
    session.add(
        DuelMember(
            duel_id=duel.id,
            user_id=created_by,
            role="challenger",
            status="accepted",
        )
    )

    # opponent
    session.add(
        DuelMember(
            duel_id=duel.id,
            user_id=opponent_user_id,
            role="opponent",
            status="invited",
        )
    )

    await session.commit()
    await session.refresh(duel)
    return duel


async def get_duel(session: AsyncSession, duel_id: int) -> Duel | None:
    stmt = select(Duel).where(Duel.id == duel_id).limit(1)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def get_member(session: AsyncSession, duel_id: int, user_id: int) -> DuelMember | None:
    stmt = (
        select(DuelMember)
        .where(DuelMember.duel_id == duel_id)
        .where(DuelMember.user_id == user_id)
        .limit(1)
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def accept_duel(session: AsyncSession, duel_id: int, user_id: int) -> bool:
    duel = await get_duel(session, duel_id)
    if not duel or duel.status != "pending":
        return False

    member = await get_member(session, duel_id, user_id)
    if not member or member.status != "invited":
        return False

    member.status = "accepted"

    # اگر همه accepted شدند → duel active
    stmt = select(DuelMember).where(DuelMember.duel_id == duel_id)
    res = await session.execute(stmt)
    members = res.scalars().all()

    if members and all(m.status == "accepted" for m in members):
        duel.status = "active"

    await session.commit()
    return True


async def decline_duel(session: AsyncSession, duel_id: int, user_id: int) -> bool:
    duel = await get_duel(session, duel_id)
    if not duel or duel.status != "pending":
        return False

    member = await get_member(session, duel_id, user_id)
    if not member or member.status != "invited":
        return False

    member.status = "declined"
    duel.status = "cancelled"

    await session.commit()
    return True
