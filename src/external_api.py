import os
import requests
from dotenv import load_dotenv  # <--- Это важно!
from typing import Optional, Union

# Загружаем переменные из .env (это исправляет вторую ошибку)
load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/convert"  # Исправление первой ошибки
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
HEADERS = {"apilayer-access-key": API_KEY}


def convert_to_rubles(
    transaction: dict, commission_rate: float = 0.0  # По умолчанию комиссии нет
) -> float:
    """
    Конвертирует сумму операции в рубли.

    Args:
        transaction (dict): Словарь с данными о транзакции.
                            Обязательные поля: amount, currency.code.
        commission_rate (float): Процент комиссии за операцию (от 0 до 1).

    Returns:
        float: Сумма в рублях после вычета комиссии.
    """

    # Получаем данные о сумме и валюте
    amount_str = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]

    # Валюта уже в рублях
    if currency_code == "RUB":
        return float(amount_str)

    # Запрос к внешнему API
    params = {
        "from": currency_code,  # Исходная валюта
        "to": "RUB",  # Целевая валюта
        "amount": amount_str,  # Сумму передаём как строку
    }

    response = requests.get(API_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    rates_data = response.json()

    # Проверка наличия результата конвертации
    converted_amount = rates_data.get("result")  # Новый ключ 'result'

    # Возвращаем итоговую сумму с вычетом комиссии
    total_amount = float(converted_amount) * (1 - commission_rate)
    return total_amount
