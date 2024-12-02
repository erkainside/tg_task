from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_priority_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора приоритета.
    """
    priorities = [
        ("Низкий", 1),
        ("Средний", 2),
        ("Высокий", 3),
    ]
    keyboard = [
        [InlineKeyboardButton(text=name, callback_data=f"priority:{value}")]
        for name, value in priorities
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
