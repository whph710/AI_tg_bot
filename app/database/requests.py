from app.database.models import async_session
from app.database.models import User, AiType, AiModel, Order
from sqlalchemy import select, update, delete, desc
from decimal import Decimal


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


# Функция добавления пользователя в базу данных
@connection
async def set_user(session, tg_id):
    # Выполнение запроса на выборку пользователя по его ID в Telegram
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    # Если пользователь не найден в базе данных
    if not user:
        # Создание нового пользователя и добавление его в сессию
        session.add(User(tg_id=tg_id, balance='0'))
        # Сохранение изменений в базе данных
        await session.commit()


@connection
async def get_user(session, tg_id):
    # Выполнение запроса на выборку пользователя по его ID в Telegram
    return await session.scalar(select(User).where(User.tg_id == tg_id))


@connection
async def get_users(session):
    # Выполнение запроса на выборку пользователя по его ID в Telegram
    return await session.scalars(select(User))


@connection
async def calculate(session, tg_id, summ, model_name, user):
    model = await session.scalar(select(AiModel).where(AiModel.name == model_name))
    new_balance = Decimal(Decimal(user.balance) - Decimal(Decimal(summ) * Decimal(model.price)))
    await session.execute(update(User).where(User.id == user.id).values(balance=str(new_balance)))
    await session.commit()



