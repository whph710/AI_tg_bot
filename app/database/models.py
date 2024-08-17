from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

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


# Асинхронная функция для создания таблиц в базе данных
async def async_main():
    # Создание подключения к базе данных
    async with engine.begin() as conn:
        # Создание таблиц в базе данных
        await conn.run_sync(Base.metadata.create_all)
