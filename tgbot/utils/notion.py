from notion_client import Client
from data import config


# Инициализация клиента Notion
notion = Client(auth=config.NOTION_TOKEN)

async def save_to_notion(user_id: int, tg_id: int, link: str, category: str, priority: int, joined_at: str) -> bool:
    """
    Сохраняет данные пользователя в базу данных Notion.
    """
    try:
        # Добавление новой страницы в базу данных
        notion.pages.create(
            parent={"database_id": config.NOTION_DATABASE_ID},
            properties={
                "Title": {  # Название первого столбца в Notion должно быть "Name"
                    "title": [{"text": {"content": f"User {user_id}"}}]  # Записываем в Title
                },
                "Telegram ID": {"number": tg_id},  # Тип "Number"
                "url": {"url": link},  # Тип "URL"
                "category": {"rich_text": [{"text": {"content": category}}]},  # Тип "Rich Text" для категорий
                "priority": {"number": priority},  # Тип "Number" для приоритета
                "Joined_at": {"date": {"start": joined_at}},  # Тип "Date", формат ISO 8601
            }
        )
        return True
    except Exception as e:
        print(f"Ошибка сохранения в Notion: {e}")
        return False
