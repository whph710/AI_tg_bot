import os
import asyncio
from aiogram import Bot, Dispatcher
from datetime import datetime
from dotenv import load_dotenv
import logging
from app.user import user
from app.admin import admin
from app.database.models import async_main


# Основная функция запуска бота
async def main():
    # Загрузка переменных окружения из файла .env
    load_dotenv()

    # Создание экземпляра бота с токеном из переменной окружения
    bot = Bot(token=os.getenv('token'))

    # Создание диспетчера для обработки сообщений
    dp = Dispatcher()

    # Добавление роутеров для пользователей и администраторов
    dp.include_routers(user, admin)

    # Регистрация функции запуска при старте бота
    dp.startup.register(on_startup)

    # Удаление вебхука и запуск поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Функция запуска при старте бота
async def on_startup(dispatcher):
    # Выполнение функции инициализации базы данных
    await async_main()


# Основная точка входа в программу
if __name__ == '__main__':
    # Запись времени запуска бота
    time_start = datetime.now()

    # Настройка логирования
    logging.basicConfig(level=logging.logMultiprocessing,
                        filename='app.log',
                        filemode='w')

    try:
        # Вывод сообщения о запуске бота
        print('-' * 36 + '\n' + 'Bot started!')

        # Запуск основной функции бота
        asyncio.run(main())
    except KeyboardInterrupt:
        # Вывод сообщения о времени работы бота и его остановке
        print('-' * 36 + '\n' + 'Bot was working for ', datetime.now() - time_start)
        print('-' * 36 + '\n' + 'Bot stopped!\n' + '-' * 36 + '\n')
