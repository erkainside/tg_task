from aiogram import Router
from aiogram.filters import CommandStart, Command

from handlers.commands import start_command_handler, start_add_command
from handlers.messages import (
    message_handler,
    forward_source_handler,
    process_url,
    category_callback_handler,
    priority_callback_handler
)
from handlers.callbacks import save_link_callback_handler, skip_link_callback_handler
from states.states import AddLink
from aiogram.filters import StateFilter


def setup() -> Router:
    router = Router()

    # Команды
    router.message.register(start_command_handler, CommandStart())
    router.message.register(start_add_command, Command("add"))

    # FSM для добавления ссылки
    router.message.register(process_url, StateFilter(AddLink.waiting_for_url))
    router.message.register(priority_callback_handler, StateFilter(AddLink.waiting_for_priority))

    # Callback для кнопок
    router.callback_query.register(category_callback_handler, lambda callback: callback.data.startswith("category:"))
    router.callback_query.register(priority_callback_handler, lambda callback: callback.data.startswith("priority:"))
    router.callback_query.register(save_link_callback_handler, lambda callback: callback.data.startswith("save:"))
    router.callback_query.register(skip_link_callback_handler, lambda callback: callback.data.startswith("skip:"))

    # Основной обработчик сообщений
    router.message.register(forward_source_handler, lambda message: message.forward_from or message.forward_from_chat)
    router.message.register(message_handler, lambda message: not message.forward_from and not message.forward_from_chat)

    return router
