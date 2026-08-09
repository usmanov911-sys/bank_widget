import logging

logger = logging.getLogger("masking")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(filename="logs/masks.log", mode="w")  # w — перезапись!
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """
    Маска для карт: XXXX XXXX **** **** XXXX
    """
    if len(card_number) != 16:
        logger.error(f"Неверная длина номера карты ({len(card_number)} символов): {card_number}")
        raise ValueError("Карточный номер должен быть ровно 16 знаков")

    first_part = card_number[:6]
    last_part = card_number[-4:]

    masked = f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"

    logger.info(f"Маскировка карты: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маска для счетов: *XXX******
    """
    if len(account_number.strip()) < 4:
        logger.error(f"Счёт слишком короткий ({account_number})")
        raise ValueError("Недостаточно символов")

    parts = account_number.split(maxsplit=1)

    if len(parts) > 1:
        label = parts[0].strip()
        number = parts[1].strip()
    else:
        label = ""
        number = account_number.strip()

    stars_count = max(len(number) - 4, 0)
    masked_number = f"{''.join(['*'] * stars_count)}{number[-4:]}"

    result = f"{label} {masked_number}".strip()

    return result


def mask_account_card(input_data: str):
    """Универсальный метод маскировки для счёта или карты"""

    cleaned_input = input_data.replace(" ", "")

    if len(cleaned_input) >= 20:
        parts = input_data.rsplit(maxsplit=1)

        try:
            label = parts[0].strip()
            number = parts[1].strip()

            masked_number = get_mask_account(number)
            result = f"{label} {masked_number}"
        except IndexError:
            logger.error(f"Попытка замаскировать неверные данные: '{input_data}'")
            raise ValueError("Некорректные входные данные")

    else:
        result = get_mask_card_number(cleaned_input)

    logger.info(f"Универсальная маска применена к строке: {result}")
    return result
