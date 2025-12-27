import re
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.steps_repo import upsert_steps_for_day


STEPS_REGEX = re.compile(r"(?:steps|step|قدم)\s*[:=]?\s*([\d,]+)", re.IGNORECASE)


def extract_steps(text: str) -> int | None:
    text = text.strip()
    m = STEPS_REGEX.search(text)
    if not m:
        return None
    raw = m.group(1).replace(",", "")
    if not raw.isdigit():
        return None
    return int(raw)


async def handle_steps_message(session: AsyncSession, user_id: int, chat_id: int, steps: int) -> str:
    today = datetime.utcnow().date()
    await upsert_steps_for_day(session, user_id, chat_id, today, steps)
    return f"✅ قدم‌های امروز ثبت شد: {steps:,} قدم"

