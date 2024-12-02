from aiogram.fsm.state import State, StatesGroup

class AddLink(StatesGroup):
    waiting_for_url = State()  # Ожидает URL
    waiting_for_category = State()  # Ожидает ввод категории
    waiting_for_priority = State()  # Ожидает ввод приоритета
