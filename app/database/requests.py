from app.database.models import async_session
from app.database.models import User, AiType, AiModel, Order
from sqlalchemy import select, update, delete, desc
from decimal import Decimal


# Функция добавления пользователя в базу данных
async def set_user(tg_id):
    # Создание асинхронной сессии для работы с базой данных
    async with async_session() as session:
        # Выполнение запроса на выборку пользователя по его ID в Telegram
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        # Если пользователь не найден в базе данных
        if not user:
            # Создание нового пользователя и добавление его в сессию
            session.add(User(tg_id=tg_id, balance='0'))
            # Сохранение изменений в базе данных
            await session.commit()


async def get_user(tg_id):
    # Создание асинхронной сессии для работы с базой данных
    async with async_session() as session:
        # Выполнение запроса на выборку пользователя по его ID в Telegram
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def calculate(tg_id, summ, model_name, user):
    # Создание асинхронной сессии для работы с базой данных
    async with async_session() as session:
        model = await session.scalar(select(AiModel).where(AiModel.name == model_name))
        new_balance = Decimal(Decimal(user.balance) - Decimal(Decimal(summ) * Decimal(model.price)))
        await session.execute(update(User).where(User.id == user.id).values(balance=str(new_balance)))
        await session.commit()