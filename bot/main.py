import asyncio
import logging
from bot.handlers.steps import router as steps_router

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.models.db import SessionLocal
from bot.jobs.sleep_reminders import find_latest_open_sessions_missing_gm
from bot.handlers.sleep import router as sleep_router
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import BOT_TOKEN, DEFAULT_TIMEZONE


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()
dp.include_router(sleep_router)
dp.include_router(steps_router)


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
    scheduler = AsyncIOScheduler(timezone=DEFAULT_TIMEZONE)

    async def sleep_reminder_job():
        async with SessionLocal() as session:
            sessions = await find_latest_open_sessions_missing_gm(session, hours=12)


            logger.info(f"[sleep_reminder_job] found {len(sessions)} sessions missing GM")

            for s in sessions:
                try:
                    logger.info(f"[sleep_reminder_job] sending reminder to chat_id={s.chat_id}, user_id={s.user_id}, session_id={s.id}")

                    mention = f"<a href='tg://user?id={s.user_id}'>این نِرد</a>"
                    await bot.send_message(
                        s.chat_id,
                        f"{mention} یادآوری ⏰\n"
                        "به نظر میاد GN ثبت شده ولی هنوز GM ثبت نشده. "
                        "اگه بیدار شدی، یه GM بزن ✅",
                        parse_mode="HTML",
                        disable_web_page_preview=True,
                    )

                    # ثبت اینکه یادآوری ارسال شده
                    from datetime import datetime, timezone
                    s.reminded_at = datetime.now(timezone.utc)
                    await session.commit()

                    logger.info(f"[sleep_reminder_job] sent ✅ session_id={s.id}")

                except Exception as e:
                    logger.exception(f"[sleep_reminder_job] failed ❌ session_id={s.id} error={e}")


    scheduler.add_job(sleep_reminder_job, "interval", minutes=5)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

