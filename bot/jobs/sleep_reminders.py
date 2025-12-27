from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.sleep import SleepSession


async def find_latest_open_sessions_missing_gm(session: AsyncSession, hours: int = 12):
    """
    فقط آخرین سشنِ باز برای هر (user_id, chat_id) که:
    - gm_at ندارد
    - reminded_at ندارد
    - و از gn_at حداقل X ساعت گذشته
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    # همه سشن‌های candidate
    stmt = (
        select(SleepSession)
        .where(SleepSession.gm_at.is_(None))
        .where(SleepSession.reminded_at.is_(None))
        .where(SleepSession.gn_at <= cutoff)
        .order_by(SleepSession.user_id.asc(), SleepSession.chat_id.asc(), SleepSession.gn_at.desc())
    )

    res = await session.execute(stmt)
    sessions = res.scalars().all()

    # انتخاب فقط آخرین سشن برای هر user/chat
    latest_map = {}
    for s in sessions:
        key = (s.user_id, s.chat_id)
        if key not in latest_map:
            latest_map[key] = s

    return list(latest_map.values())


