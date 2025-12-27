import asyncio
import logging

from bot.handlers.sleep import router as sleep_router
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import BOT_TOKEN, DEFAULT_TIMEZONE


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()
dp.include_router(sleep_router)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "سلام! من Nerdassistant هستم 🤖\n"
        "فعلاً در حال راه‌اندازی‌ام. به زودی Sleep Protocol و Duel فعال می‌شن ✅"
    )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Set it in .env")

    logger.info("Nerdassistant bot is starting...")
    logger.info(f"Timezone: {DEFAULT_TIMEZONE}")

    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

