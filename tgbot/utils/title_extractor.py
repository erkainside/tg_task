from bs4 import BeautifulSoup
import ssl
import certifi
from aiohttp import ClientSession, TCPConnector

async def fetch_title(url: str) -> str:
    """
    Извлекает заголовок страницы по указанной ссылке с использованием certifi.
    """
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)
        async with ClientSession(connector=connector) as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.string if soup.title else "No Title"
                    return title.strip()
                else:
                    return f"HTTP Error {response.status}"
    except Exception as e:
        return f"Error: {e}"

