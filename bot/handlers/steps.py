from aiogram import Router
from aiogram.types import Message

from bot.models.db import SessionLocal
from bot.services.steps_service import extract_steps, handle_steps_message

router = Router()


@router.message()
async def steps_listener(message: Message):
    if not message.text:
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
