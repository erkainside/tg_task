from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_category_keyboard(categories: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=category, callback_data=f"category:{category}")]
            for category in categories
        ]
    )