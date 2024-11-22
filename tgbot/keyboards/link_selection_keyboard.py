from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_link_confirmation_keyboard(link: str) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками "Сохранить" и "Пропустить" для конкретной ссылки.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сохранить", callback_data=f"save:{link}"),
            InlineKeyboardButton(text="Пропустить", callback_data=f"skip:{link}")
        ]
    ])
    return keyboard
