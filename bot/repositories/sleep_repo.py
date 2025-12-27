from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.sleep import SleepSession


async def create_gn(session: AsyncSession, user_id: int, chat_id: int) -> SleepSession:
    now = datetime.now(timezone.utc)
    sleep = SleepSession(user_id=user_id, chat_id=chat_id, gn_at=now, gm_at=None)
    session.add(sleep)
    await session.commit()
    await session.refresh(sleep)
    return sleep


async def set_gm_for_latest_open_session(
    session: AsyncSession, user_id: int, chat_id: int
) -> SleepSession | None:
    # آخرین سشن خواب که gm_at هنوز null است
    stmt = (
        select(SleepSession)
        .where(SleepSession.user_id == user_id, SleepSession.chat_id == chat_id, SleepSession.gm_at.is_(None))
        .order_by(SleepSession.gn_at.desc())
        .limit(1)
    )
    res = await session.execute(stmt)
    sleep = res.scalar_one_or_none()
    if not sleep:
        return None

    sleep.gm_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(sleep)
    return sleep

