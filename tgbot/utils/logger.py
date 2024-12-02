from aiogram import Bot
from data import config

async def log_to_channel(bot: Bot, message: str):
    """
    Отправляет сообщение в указанный Telegram-канал.
    """
    try:
        await bot.send_message(chat_id=config.LOG_CHANNEL_ID, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в канал: {e}")
