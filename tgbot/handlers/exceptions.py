import logging
from aiogram import types
from aiogram.handlers import ErrorHandler

class CustomErrorHandler(ErrorHandler):
    async def handle(self, update: types.Update, exception: Exception) -> bool:
        """
        Обрабатывает все исключения в боте и отправляет сообщение пользователю.
        """
        logging.error(f"Произошла ошибка: {exception}")

        # Отправляем сообщение пользователю (если возможно)
        if update.message:
            await update.message.answer("Произошла ошибка. Пожалуйста, попробуйте снова или обратитесь к администратору.")

        # Отправляем сообщение в лог-канал (если у вас есть канал логов)
        LOG_CHANNEL_ID = -1001234567890  # Замените на ваш канал
        try:
            bot = update.message.bot
            await bot.send_message(
                chat_id=LOG_CHANNEL_ID,
                text=f"Ошибка: {exception}\n\nОбновление: {update}"
            )
        except Exception as log_exception:
            logging.error(f"Не удалось отправить сообщение об ошибке в лог-канал: {log_exception}")

        # Возвращаем True, чтобы не мешать другим обработчикам
        return True
