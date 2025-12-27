import re
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
]

GM_PATTERNS = [
    r"\bgm\b",
    r"\bgood\s*morning\b",
    r"صبح\s*بخیر",
    r"صبح‌بخیر",
    r"صبحت\s*بخیر",
    r"☀️",
    r"🌞",
]


def matches_any(text: str, patterns: list[str]) -> bool:
    text = text.strip().lower()
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            return True
    return False


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

