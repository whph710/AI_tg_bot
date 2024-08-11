import os
import asyncio
from aiogram import Bot, Dispatcher
from datetime import datetime
from dotenv import load_dotenv
import logging
from app.user import user
from app.admin import admin


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('token'))
    dp = Dispatcher()
    dp.include_routers(user, admin)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    time_start = datetime.now()
    logging.basicConfig(level=logging.logMultiprocessing,
                        filename='app.log',
                        filemode='w')
    try:
        print('-' * 36 + '\n' + 'Bot started!')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('-' * 36 + '\n' + 'Bot was working for ', datetime.now() - time_start)
        print('-' * 36 + '\n' + 'Bot stopped!\n' + '-' * 36 + '\n')
