from aiogram import types
from aiogram.fsm.context import FSMContext
from states.states import AddLink
from handlers.messages import create_category_keyboard, CATEGORIES

async def save_link_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки "Сохранить", запрашивает категорию и сохраняет данные в SQLite и Notion.
    """
    link = ":".join(callback.data.split(":")[1:])  # Извлекаем ссылку, учитывая наличие двоеточий
    print(f"Ссылка для сохранения: {link}")  # Лог для проверки

    # Сохраняем ссылку в состоянии
    await state.update_data(link=link)

    # Запрашиваем категорию
    keyboard = create_category_keyboard(CATEGORIES)
    await callback.message.answer("Выберите категорию для этой ссылки:", reply_markup=keyboard)
    
    # Устанавливаем состояние ожидания выбор категори
    await state.set_state(AddLink.waiting_for_category)

    # Закрываем уведомление
    await callback.answer()


async def skip_link_callback_handler(callback: types.CallbackQuery):
    """
    Пропускает выбранную ссылку.
    """
    link = callback.data.split(":")[1]  # Извлекаем ссылку из callback_data
    await callback.message.answer(f"Ссылка пропущена: {link}")
    await callback.answer()
