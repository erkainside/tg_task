def determine_social_source(url: str) -> dict:
    """
    Определяет источник и детали по URL.
    Возвращает словарь с информацией.
    """
    from urllib.parse import urlparse
    import re

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    path = parsed_url.path

    patterns = {
        "YouTube": {
            "pattern": r"(?:www\.)?youtube\.com|youtu\.be",
            "details": lambda: {"video_id": path.split("/")[-1]} if "watch" in path or "youtu.be" in domain else {}
        },
        "Instagram": {
            "pattern": r"(?:www\.)?instagram\.com",
            "details": lambda: {"username": path.split("/")[1]} if len(path.split("/")) > 1 else {}
        },
        "Twitter": {
            "pattern": r"(?:www\.)?twitter\.com",
            "details": lambda: {"username": path.split("/")[1]} if len(path.split("/")) > 1 else {}
        },
        "TikTok": {
            "pattern": r"(?:www\.)?tiktok\.com",
            "details": lambda: {"username": path.split("/")[1]} if len(path.split("/")) > 1 else {}
        },
        "Facebook": {
            "pattern": r"(?:www\.)?facebook\.com",
            "details": lambda: {"page_or_user": path.split("/")[1]} if len(path.split("/")) > 1 else {}
        },
    }

    for platform, data in patterns.items():
        if re.search(data["pattern"], domain):
            return {
                "platform": platform,
                **data["details"]()
            }

    return {"platform": "Unknown", "details": {}}
