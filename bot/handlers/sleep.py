import re
from aiogram.filters import Command
from aiogram.types import FSInputFile
from bot.repositories.sleep_repo import get_sleep_sessions_last_days
from bot.charts.sleep_weekly import build_sleep_weekly_chart
from aiogram import Router
from aiogram.types import Message

from bot.models.db import SessionLocal
from bot.services.sleep_service import handle_gn, handle_gm

router = Router()

GN_PATTERNS = [
    r"\bgn\b",
    r"\bgood\s*night\b",
    r"شب\s*بخیر",
    r"شب‌بخیر",
    r"شبت\s*بخیر",
    r"😴",
    r"🌙",
    r"\boyasumi\b",
]

GM_PATTERNS = [
    r"\bgm\b",
    r"\bgood\s*morning\b",
    r"صبح\s*بخیر",
    r"صبح‌بخیر",
    r"صبحت\s*بخیر",
    r"☀️",
    r"🌞",
    r"\bohio\b",
    r"اوهایو",
]


def matches_any(text: str, patterns: list[str]) -> bool:
    text = text.strip().lower()
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            return True
    return False

@router.message(Command("sleep_weekly"))
async def sleep_weekly_report(message: Message):
    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    if user_id == 0:
        return

    async with SessionLocal() as session:
        sessions = await get_sleep_sessions_last_days(session, user_id, chat_id, days=7)

    chart_path = build_sleep_weekly_chart(sessions, out_dir="/tmp")
    photo = FSInputFile(chart_path)

    await message.answer_photo(
        photo=photo,
        caption="📊 گزارش هفتگی خواب (۷ روز اخیر)"
    )


@router.message()
async def sleep_listener(message: Message):
    if not message.text:
        return

    text = message.text
    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id

    if user_id == 0:
        return

    if matches_any(text, GN_PATTERNS):
        async with SessionLocal() as session:
            reply = await handle_gn(session, user_id, chat_id)
        await message.reply(reply)
        return

    if matches_any(text, GM_PATTERNS):
        async with SessionLocal() as session:
            reply = await handle_gm(session, user_id, chat_id)
        await message.reply(reply)
        return

