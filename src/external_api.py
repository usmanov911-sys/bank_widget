import os
import requests
from dotenv import load_dotenv
from typing import Optional, Union

load_dotenv()

API_URL = "http://api.exchangerate-api.com/v4/latest/"
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
HEADERS = {"apilayer-access-key": API_KEY}


def convert_to_rubles(transaction: dict) -> float:
    """
    Конвертирует сумму операции в рубли.

    Если валюта USD или EUR, запрашивает текущий курс у внешнего API.
    Для других валют просто возвращает исходную сумму.

    Args:
        transaction (dict): Словарь с данными о транзакции.
                            Обязательные поля: amount, currency.code.

    Returns:
        float: Сумма в рублях.
    """
    amount_str = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]

    # Валюта уже в рублях
    if currency_code == "RUB":
        return float(amount_str)

    # Запрос курса к внешнему API
    response = requests.get(API_URL + currency_code, headers=HEADERS)
    response.raise_for_status()
    rates_data = response.json()

    # Получаем курс к рублю
    rate_to_rub = rates_data["rates"].get("RUB")

    # Возвращаем None, если нет данных о курсе
    if not rate_to_rub:
        raise ValueError(f"No exchange rate found for {currency_code} to RUB.")

    return float(amount_str) * rate_to_rub
