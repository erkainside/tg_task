from database.sqlite import async_session
from database.sqlite import User
from sqlalchemy import select, update, delete, desc
from datetime import datetime


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, joined_at=datetime.utcnow()))
            await session.commit()


async def update_user_link(tg_id: int, link: str) -> bool:
    async with async_session() as session:
        # Проверяем, существует ли пользователь
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            # Обновляем ссылку
            await session.execute(
                update(User).where(User.tg_id == tg_id).values(link=link)
            )
            await session.commit()
            return True
        else:
            return False  # Пользователь не найден


async def get_user_data(tg_id: int):
    """
    Извлекает все данные пользователя из SQLite.
    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalars().all()  # Возвращает список записей для пользователя



async def save_user(tg_id: int, link: str, category: str, priority: int):
    """
    Сохраняет новую запись для пользователя с указанной ссылкой, категорией и приоритетом.
    """
    async with async_session() as session:
        # Создаём новую запись
        new_entry = User(
            tg_id=tg_id,
            link=link,
            category=category,
            priority=priority,
            joined_at=datetime.utcnow()
        )
        session.add(new_entry)  # Добавляем запись
        await session.commit()  # Применяем изменения

