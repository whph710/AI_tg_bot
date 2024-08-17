from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, desc


# Функция добавления пользователя в базу данных
async def set_user(tg_id):
    # Создание асинхронной сессии для работы с базой данных
    async with async_session() as session:
        # Выполнение запроса на выборку пользователя по его ID в Telegram
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        # Если пользователь не найден в базе данных
        if not user:
            # Создание нового пользователя и добавление его в сессию
            session.add(User(tg_id=tg_id))
            # Сохранение изменений в базе данных
            await session.commit()
