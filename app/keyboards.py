from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Генератор текста')],
], resize_keyboard=True, input_field_placeholder='Выберите действие', one_time_keyboard=True)