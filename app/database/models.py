from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

# Создание подключения к базе данных SQLite
engine = create_async_engine(
    url='sqlite+aiosqlite:///db.sqlite3',  # URL подключения к базе данных
    echo=True  # Выводить в консоль все SQL запросы
)

# Создание сессии для работы с базой данных
async_session = async_sessionmaker(engine)


# Создание базового класса для моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Создание модели пользователя
class User(Base):
    # Название таблицы в базе данных
    __tablename__ = 'users'

    # Поле id - первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # Поле tg_id - идентификатор пользователя в Telegram
    tg_id = mapped_column(BigInteger)
    # Поле balance - баланс пользователя
    balance: Mapped[str] = mapped_column(String(15))


# Создание модели типа AI
class AiType(Base):
    __tablename__ = 'ai_types'

    # Поле id - первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # Поле name - название типа AI
    name: Mapped[str] = mapped_column(String(25))


# Создание модели модели AI
class AiModel(Base):
    __tablename__ = 'ai_models'

    # Поле id - первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # Поле name - название модели AI
    name: Mapped[str] = mapped_column(String(25))
    # Поле ai_type - тип AI, ссылка на таблицу ai_types
    ai_type: Mapped[int] = mapped_column(ForeignKey('ai_types.id'))
    # Поле price - цена модели AI
    price: Mapped[str] = mapped_column(String(25))


# Создание модели заказа
class Order(Base):
    __tablename__ = 'orders'

    # Поле id - первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # Поле status - статус заказа
    status: Mapped[str] = mapped_column(String(50))
    # Поле user - пользователь, который сделал заказ, ссылка на таблицу users
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # Поле amount - сумма заказа
    amount: Mapped[str] = mapped_column(String(15))
    # Поле created_at - дата создания заказа
    created_at: Mapped[datetime]
    # Поле order - описание заказа
    order: Mapped[str] = mapped_column(String(100))


# Асинхронная функция для создания таблиц в базе данных
async def async_main():
    # Создание подключения к базе данных
    async with engine.begin() as conn:
        # Создание таблиц в базе данных
        await conn.run_sync(Base.metadata.create_all)
