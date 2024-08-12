from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from app.states import Chat
from aiogram.fsm.context import FSMContext
from app.generators import gpt_text
user = Router()


@user.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n', reply_markup=kb.main)


@user.message(F.text == 'Генератор текста')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer(f'Введи ваш запрос')


@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    response = await gpt_text(message.text, 'gpt-3.5-turbo')
    await message.answer(response)

