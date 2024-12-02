from aiogram import types
from aiogram.fsm.context import FSMContext
import database.requests as rq
from states.states import AddLink


async def start_add_command(message: types.Message, state: FSMContext):
    """
    Начинает процесс добавления ссылки через команду /add.
    """
    await message.answer("Введите ссылку для сохранения:")
    await state.set_state(AddLink.waiting_for_url)


async def start_command_handler(message: types.Message, state: FSMContext):
    from_user = message.from_user
    greeting_text = f"Приветствую, {from_user.full_name}! Чем могу помочь?"
    await rq.set_user(message.from_user.id)
    await message.answer(greeting_text)
