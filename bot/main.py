import asyncio
from bot.config import DEFAULT_TIMEZONE

async def main():
    print("Nerdassistant bot is booting...")
    print(f"Timezone: {DEFAULT_TIMEZONE}")
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

