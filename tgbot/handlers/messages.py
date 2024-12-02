from aiogram import types, Bot
from datetime import datetime
from aiogram.fsm.context import FSMContext
from states.states import AddLink
from utils.text_processing import extract_link_from_message
from utils.title_extractor import fetch_title
from utils.social_source import determine_social_source
from database.requests import set_user, save_user
from utils.notion import save_to_notion
from utils.logger import log_to_channel
from keyboards.category_keyboard import create_category_keyboard
from keyboards.priority_keyboard import create_priority_keyboard
from keyboards.link_selection_keyboard import create_link_confirmation_keyboard



async def message_handler(message: types.Message, bot: Bot):

    if message.text.startswith("/"):
        return
    
    text = message.text
    links = extract_link_from_message(text)  # Извлекаем все ссылки

    try:
        if not links:
            await message.answer("Ссылки не найдены в вашем сообщении. Попробуйте снова!")
            return

        # Регистрируем пользователя, если его нет
        await set_user(message.from_user.id)

        # Для каждой ссылки предлагаем сохранить или пропустить
        for link in links:
            # Определяем источник (соцсеть или веб-страница)
            source_info = determine_social_source(link)
            platform = source_info["platform"]

            # Получаем заголовок страницы, если это не соцсеть
            title = await fetch_title(link) if platform == "Unknown" else platform

            # Отправляем сообщение с кнопками
            keyboard = create_link_confirmation_keyboard(link)
            await message.answer(
                f"Платформа: {platform}\nЗаголовок: {title}\nХотите сохранить эту ссылку?\n{link}",
                reply_markup=keyboard
            )
    except:
        await message.answer("Ссылки не найдены в вашем сообщении. Попробуйте снова!")
        return



async def forward_source_handler(message: types.Message):
    """
    Обрабатывает пересланные сообщения, определяет источник и платформу ссылок.
    """
    if message.forward_from:
        # Переслано от пользователя
        source = f"Пользователь: {message.forward_from.full_name} (ID: {message.forward_from.id})"
        if message.forward_from.username:
            source += f", Username: @{message.forward_from.username}"
    elif message.forward_from_chat:
        # Переслано из чата, группы или канала
        source = f"Чат/Канал: {message.forward_from_chat.title} (ID: {message.forward_from_chat.id})"
        if message.forward_from_chat.username:
            source += f", Username: @{message.forward_from_chat.username}"
    else:
        source = "Это не пересланное сообщение."

    # Извлекаем ссылки из текста пересланного сообщения (если есть)
    links = extract_link_from_message(message.text or "")
    if links:
        response = f"Источник сообщения:\n{source}\n\nСсылки в сообщении:\n"
        for link in links:
            source_info = determine_social_source(link)
            platform = source_info["platform"]
            response += f"- {link} (Платформа: {platform})\n"
    else:
        response = f"Источник сообщения:\n{source}\n\nСсылки не найдены."

    await message.answer(response)


async def show_categories_handler(message: types.Message):
    """
    Отправляет список категорий с инлайн-кнопками.
    """
    keyboard = create_category_keyboard(CATEGORIES)
    await message.answer("Выберите категорию:", reply_markup=keyboard)


CATEGORIES = ["Новости", "Спорт", "Технологии", "Развлечения", "Музыка"]

async def process_url(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод ссылки и запрашивает категорию.
    """
    # Проверяем, есть ли текст в сообщении

    if not message.text:
        await message.answer("Сообщение не содержит текста. Отправьте текст с ссылкой.")
        return

    # Убираем лишние пробелы
    text = message.text.strip()
    links = extract_link_from_message(text)

    if not links:
        await message.answer("Введите корректную ссылку.")
        return

    link = links[0]  # Берём первую ссылку

    # Сохраняем ссылку в состоянии
    await state.update_data(link=link)

    # Предлагаем пользователю выбрать категорию из кнопок
    keyboard = create_category_keyboard(CATEGORIES)
    await message.answer("Выберите категорию для этой ссылки:", reply_markup=keyboard)
    await state.set_state(AddLink.waiting_for_category)


async def category_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор категории через инлайн-кнопки.
    """
    category = callback.data.split(":")[1]
    await state.update_data(category=category)

    # Отправляем клавиатуру с приоритетами
    keyboard = create_priority_keyboard()
    await callback.message.answer("Выберите приоритет для этой ссылки:", reply_markup=keyboard)

    # Устанавливаем состояние ожидания выбора приоритета
    await state.set_state(AddLink.waiting_for_priority)
    await callback.answer()


async def priority_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор приоритета.
    """
    priority = int(callback.data.split(":")[1])  # Извлекаем приоритет из callback_data

    # Сохраняем приоритет в состоянии
    await state.update_data(priority=priority)

    # Извлекаем данные из состояния
    data = await state.get_data()
    link = data["link"]
    category = data["category"]

    # Сохраняем в SQLite
    await save_user(
        tg_id=callback.from_user.id,
        link=link,
        category=category,
        priority=priority
    )

    # Сохраняем в Notion
    notion_success = await save_to_notion(
        user_id=callback.from_user.id,
        tg_id=callback.from_user.id,
        link=link,
        category=category,
        priority=priority,
        joined_at=datetime.utcnow().isoformat()
    )

    if notion_success:
        # Уведомляем пользователя об успешном сохранении
        await callback.message.answer(
            f"Ссылка успешно сохранена:\nURL: {link}\nКатегория: {category}\nПриоритет: {priority}"
        )

        # Логирование в Telegram-канал
        log_message = (
            f"Пользователь: {callback.from_user.full_name} (ID: {callback.from_user.id})\n"
            f"Ссылка: {link}\n"
            f"Категория: {category}\n"
            f"Приоритет: {priority}\n"
            f"Дата сохранения: {datetime.utcnow().isoformat()}"
        )
        await log_to_channel(callback.message.bot, log_message)
    else:
        # Уведомляем о проблемах с сохранением в Notion
        await callback.message.answer("Ошибка: данные сохранены в SQLite, но не удалось сохранить в Notion.")

    # Очищаем состояние
    await state.clear()
    await callback.answer()
