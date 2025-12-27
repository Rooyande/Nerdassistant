from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile
from bot.repositories.steps_repo import get_steps_last_days
from bot.charts.steps_weekly import build_steps_weekly_chart

from bot.models.db import SessionLocal
from bot.services.steps_service import extract_steps, handle_steps_message

router = Router()

@router.message(Command("steps_weekly"))
async def steps_weekly_report(message: Message):
    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    if user_id == 0:
        return

    async with SessionLocal() as session:
        entries = await get_steps_last_days(session, user_id, chat_id, days=7)

    chart_path = build_steps_weekly_chart(entries, out_dir="/tmp")
    photo = FSInputFile(chart_path)

    await message.answer_photo(
        photo=photo,
        caption="📊 گزارش هفتگی قدم‌ها (۷ روز اخیر)"
    )

from aiogram import F

@router.message(F.text.regexp(r"(?i)^(steps|step|قدم)\s*[:=]?\s*[\d,]+$"))
async def steps_listener(message: Message):

    if not message.text:
        return
    if message.text.strip().startswith("/"):
        return

    steps = extract_steps(message.text)
    if steps is None:
        return

    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    if user_id == 0:
        return

    # محدودیت ساده برای جلوگیری از اعداد عجیب
    if steps < 0 or steps > 200_000:
        await message.reply("عدد قدم‌ها غیرمنطقیه 😅 (۰ تا ۲۰۰,۰۰۰)")
        return

    async with SessionLocal() as session:
        reply = await handle_steps_message(session, user_id, chat_id, steps)

    await message.reply(reply)
