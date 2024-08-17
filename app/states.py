from aiogram.fsm.state import StatesGroup, State


# Создание класса для управления состоянием диалога
class Chat(StatesGroup):
    # Состояние ожидания ввода текста
    text = State()
    # Состояние ожидания ответа
    wait = State()
