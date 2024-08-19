from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.states import Chat, Image
from aiogram.fsm.context import FSMContext
from app.generators import gpt_text, gpt_image
from app.database.requests import set_user, get_user, calculate
from decimal import Decimal


# Создание экземпляра роутера для обработки сообщений пользователей
user = Router()


@user.message(F.text == 'Генератор текста')
async def chatting(message: Message, state: FSMContext):
    # Проверка баланса
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        # Установка состояния диалога
        await state.set_state(Chat.text)
        # Отправка сообщения с запросом ввода текста
        await message.answer(f'Введи ваш запрос', reply_markup=kb.cancel)
    else:
        await message.answer(f'Недостаточно средств')


# Обработчик сообщений с текстом "Генератор текста"
@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        # Установка состояния ожидания ответа
        await state.set_state(Chat.wait)
        # Вызов функции генерации текста
        response = await gpt_text(message.text, 'gpt-4o')
        # Вызов функции расчета баланса
        await calculate(message.from_user.id, response['usage'], 'gpt-4o')
        # Отправка ответа
        await message.answer(response['response'])
        #
        await state.set_state(Chat.text)
    else:
        await message.answer(f'Недостаточно средств')


# Обработчик команды /start
@user.message(F.text == 'Отмена')
@user.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    # Вызов функции добавления пользователя в базу данных
    await set_user(message.from_user.id)
    # Отправка приветственного сообщения с клавиатурой
    await message.answer(f'Привет, {message.from_user.full_name}!\n', reply_markup=kb.main)
    # Очистка состояния диалога
    await state.clear()
# Обработчик сообщений в состоянии диалога Chat.text


# Обработчик сообщений в состоянии диалога Chat.wait
@user.message(Image.wait)
@user.message(Chat.wait)
async def wait_response(message: Message):
    # Отправка сообщения с информацией о задержке
    await message.answer('Ваш запрос обрабатывается...')


@user.message(F.text == 'Генератор изображения')
async def chatting(message: Message, state: FSMContext):
    # Проверка баланса
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        # Установка состояния диалога
        await state.set_state(Image.text)
        # Отправка сообщения с запросом ввода текста
        await message.answer(f'Введи ваш запрос', reply_markup=kb.cancel)
    else:
        await message.answer(f'Недостаточно средств')


# Обработчик сообщений с текстом "Генератор изображения"
@user.message(Image.text)
async def chat_response(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balance) > 0:
        # Установка состояния ожидания ответа
        await state.set_state(Image.wait)
        # Вызов функции генерации текста
        response = await gpt_image(message.text, 'dall-e-3')
        # Вызов функции расчета баланса
        await calculate(message.from_user.id, response['usage'], 'dall-e-3')
        try:
            await message.answer_photo(photo=response['response'])
        except Exception as e:
            # Отправка ответа
            await message.answer(response['response'])
        #
        await state.set_state(Image.text)
    else:
        await message.answer(f'Недостаточно средств')




