import re

def extract_link_from_message(text: str) -> list[str]:
    """
    Извлекает все ссылки из текста сообщения.
    """
    #link_pattern = r'https?://[^\s]+'  # Регулярное выражение для поиска ссылок
    link_pattern = r'\b(?:http://|https://|www\.)\S+' # # Регулярное выражение для поиска ссылок
    
    return re.findall(link_pattern, text)
