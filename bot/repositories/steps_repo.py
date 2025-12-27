from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.steps import StepEntry


async def upsert_steps_for_day(
    session: AsyncSession, user_id: int, chat_id: int, day: date, steps: int
) -> StepEntry:
    stmt = (
        select(StepEntry)
        .where(StepEntry.user_id == user_id)
        .where(StepEntry.chat_id == chat_id)
        .where(StepEntry.day == day)
        .limit(1)
    )
    res = await session.execute(stmt)
    entry = res.scalar_one_or_none()

    if entry:
        entry.steps = steps
    else:
        entry = StepEntry(user_id=user_id, chat_id=chat_id, day=day, steps=steps)
        session.add(entry)

    await session.commit()
    await session.refresh(entry)
    return entry

from datetime import datetime, timedelta

async def get_steps_last_days(
    session: AsyncSession, user_id: int, chat_id: int, days: int = 7
):
    cutoff = datetime.utcnow().date() - timedelta(days=days)

    stmt = (
        select(StepEntry)
        .where(StepEntry.user_id == user_id)
        .where(StepEntry.chat_id == chat_id)
        .where(StepEntry.day >= cutoff)
        .order_by(StepEntry.day.asc())
    )
    res = await session.execute(stmt)
    return res.scalars().all()
