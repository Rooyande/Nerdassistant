import re
from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.models.db import SessionLocal
from bot.repositories.duel_repo import create_duel_steps, accept_duel, decline_duel


router = Router()


def _parse_days(text: str) -> int:
    # "7d" => 7
    m = re.search(r"(\d+)\s*d", text.lower())
    if not m:
        return 7
    days = int(m.group(1))
    if days < 1:
        days = 1
    if days > 30:
        days = 30
    return days


@router.message(Command("duel_steps"))
async def duel_steps_cmd(message: Message):
    """
    /duel_steps @user 7d
    """
    if not message.text:
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("فرمت درست:\n/duel_steps @username 7d")
        return

    # پیدا کردن opponent از reply یا username
    opponent_user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        opponent_user_id = message.reply_to_message.from_user.id
    else:
        # اگر ریپلای نبود، فعلاً از username پشتیبانی نمی‌کنیم (بعداً اضافه می‌کنیم)
        await message.reply("برای شروع دوئل، روی پیام طرف ریپلای کن و بنویس:\n/duel_steps 7d")
        return

    days = _parse_days(message.text)

    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    if user_id == 0 or opponent_user_id is None:
        return

    if opponent_user_id == user_id:
        await message.reply("با خودت دوئل نزن نِرد 😄")
        return

    async with SessionLocal() as session:
        duel = await create_duel_steps(session, chat_id, user_id, opponent_user_id, days=days)

    mention_opponent = f"<a href='tg://user?id={opponent_user_id}'>حریف</a>"
    mention_creator = f"<a href='tg://user?id={user_id}'>چلنجر</a>"

    await message.reply(
        f"⚔️ دوئل قدم‌ها ساخته شد!\n"
        f"{mention_creator} vs {mention_opponent}\n"
        f"مدت: {days} روز\n"
        f"برای قبول: /duel_accept {duel.id}\n"
        f"برای رد: /duel_decline {duel.id}",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@router.message(Command("duel_accept"))
async def duel_accept_cmd(message: Message):
    if not message.text:
        return

    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("فرمت درست:\n/duel_accept <duel_id>")
        return

    duel_id = int(parts[1])
    user_id = message.from_user.id if message.from_user else 0
    if user_id == 0:
        return

    async with SessionLocal() as session:
        ok = await accept_duel(session, duel_id, user_id)

    if ok:
        await message.reply(f"✅ دوئل {duel_id} قبول شد! شروع شد 🔥")
    else:
        await message.reply("❌ نتونستم دوئل رو قبول کنم (یا دوئل وجود نداره/یا دعوت تو نیست).")


@router.message(Command("duel_decline"))
async def duel_decline_cmd(message: Message):
    if not message.text:
        return

    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("فرمت درست:\n/duel_decline <duel_id>")
        return

    duel_id = int(parts[1])
    user_id = message.from_user.id if message.from_user else 0
    if user_id == 0:
        return

    async with SessionLocal() as session:
        ok = await decline_duel(session, duel_id, user_id)

    if ok:
        await message.reply(f"🚫 دوئل {duel_id} رد شد و کنسل شد.")
    else:
        await message.reply("❌ نتونستم دوئل رو رد کنم (یا دوئل وجود نداره/یا دعوت تو نیست).")
