from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.states import Chat
from aiogram.fsm.context import FSMContext
from app.generators import gpt_text
from app.database.requests import set_user

# Создание экземпляра роутера для обработки сообщений пользователей
user = Router()


# Обработчик команды /start
@user.message(CommandStart())
async def command_start(message: Message):
    # Вызов функции добавления пользователя в базу данных
    await set_user(message.from_user.id)
    # Отправка приветственного сообщения с клавиатурой
    await message.answer(f'Привет, {message.from_user.full_name}!\n', reply_markup=kb.main)


# Обработчик сообщений с текстом "Генератор текста"
@user.message(F.text == 'Генератор текста')
async def chatting(message: Message, state: FSMContext):
    # Установка состояния диалога
    await state.set_state(Chat.text)
    # Отправка сообщения с запросом ввода текста
    await message.answer(f'Введи ваш запрос')


# Обработчик сообщений в состоянии диалога Chat.text
@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    # Установка состояния ожидания ответа
    await state.set_state(Chat.wait)
    # Вызов функции генерации текста
    response = await gpt_text(message.text, 'gpt-3.5-turbo')
    # Отправка ответа
    await message.answer(response)
    # Очистка состояния диалога
    await state.clear()


# Обработчик сообщений в состоянии диалога Chat.wait
@user.message(Chat.wait)
async def wait_response(message: Message):
    # Отправка сообщения с информацией о задержке
    await message.answer('Ваш запрос обрабатывается...')
