import re

def extract_link_from_message(text: str) -> list[str]:
    """
    Извлекает все ссылки из текста сообщения.
    """
    link_pattern = r'https?://[^\s]+'  # Регулярное выражение для поиска ссылок
    return re.findall(link_pattern, text)
