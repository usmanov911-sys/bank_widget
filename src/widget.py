from src.masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(info: str) -> str:
    """Маскирует карту или счет целиком."""

    parts = info.split()
    label = " ".join(parts[:-1])
    number = parts[-1]

    if len(number) >= 20:
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)

    return f"{label} {masked}"


def get_date(iso_string: str) -> str:
    """Переводит ISO-время в формат ДД.ММ.ГГГГ"""

    dt = datetime.fromisoformat(iso_string)
    return dt.strftime("%d.%m.%Y")
