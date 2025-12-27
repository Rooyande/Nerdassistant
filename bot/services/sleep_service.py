from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.sleep_repo import create_gn, set_gm_for_latest_open_session


def _format_duration_minutes(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    if h > 0 and m > 0:
        return f"{h} ساعت و {m} دقیقه"
    if h > 0:
        return f"{h} ساعت"
    return f"{m} دقیقه"


async def handle_gn(session: AsyncSession, user_id: int, chat_id: int) -> str:
    await create_gn(session, user_id, chat_id)
    return "شب بخیر 🌙 ثبت شد ✅"


async def handle_gm(session: AsyncSession, user_id: int, chat_id: int) -> str:
    sleep = await set_gm_for_latest_open_session(session, user_id, chat_id)
    if not sleep:
        return "صبح بخیر ☀️ ولی GN قبلی پیدا نشد 😅\nلطفاً از این به بعد قبلش GN بده."

    duration = sleep.gm_at - sleep.gn_at  # type: ignore
    minutes = int(duration.total_seconds() // 60)
    if minutes < 0:
        minutes = 0

    return f"صبح بخیر ☀️ ثبت شد ✅\nمدت خواب: {_format_duration_minutes(minutes)}"
