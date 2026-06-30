def get_mask_card_number(card_number: str) -> str:
    """Маска для карт: XXXX XX** **** XXXX"""
    if len(card_number) != 16:
        raise ValueError("Карточный номер должен быть ровно 16 знаков")

    first_part = card_number[:6]
    last_part = card_number[-4:]

    masked = first_part[:4] + " " + first_part[4:] + "**" + " **** " + last_part

    return masked


def get_mask_account(account_number: str) -> str:
    """Маска для счетов: **XXXX"""
    if len(account_number) < 4:
        raise ValueError("Недостаточно символов")

    return "**" + account_number[-4:]
