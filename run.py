import asyncio

import logging

from aiogram import Bot, Dispatcher

from files.handlers.routers import *
from files.defs import *
from resources.config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(main_router)
    dp.include_router(def_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # just for debug
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
