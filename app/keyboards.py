from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создание главной клавиатуры
main = ReplyKeyboardMarkup(
    # Описание клавиатуры
    keyboard=[
        # Кнопка для вызова генератора текста
        [KeyboardButton(text='Генератор текста')],
        # Кнопка для вызова генератора изображений
        [KeyboardButton(text='Генератор изображения')],
    ],
    # Размер клавиатуры
    resize_keyboard=True,
    # Подсказка для поля ввода
    input_field_placeholder='Выберите действие',
    # Клавиатура будет скрыта после одного использования
    one_time_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отмена')]
    ],
    resize_keyboard=True
)