from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.states import Chat
from aiogram.fsm.context import FSMContext
from app.generators import gpt_text
from app.database.requests import set_user
user = Router()


@user.message(CommandStart())
async def command_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(f'Привет, {message.from_user.full_name}!\n', reply_markup=kb.main)


@user.message(F.text == 'Генератор текста')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer(f'Введи ваш запрос')


@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    await state.set_state(Chat.wait)
    response = await gpt_text(message.text, 'gpt-3.5-turbo')
    await message.answer(response)
    await state.clear()


@user.message(Chat.wait)
async def wait_response(message: Message):
    await message.answer('Ваш запрос обрабатывается...')