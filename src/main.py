import json

from datetime import datetime
from typing import List, Dict, Optional

from src.utils import load_json_file
from src.data_loader import load_csv_file, load_excel_file
from src.masks import mask_account_card
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date

current_transactions: List[Dict] = []


def print_transaction(transaction: Dict) -> None:
    """Красиво печатает одну операцию"""
    date_str = transaction.get("date", "")
    try:
        dt = datetime.fromisoformat(date_str[:-4])
        formatted_date = dt.strftime("%d.%m.%Y")
    except ValueError:
        formatted_date = ""

    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name", "")

    from_ = transaction.get("from", "")
    to_ = transaction.get("to", "")

    masked_from = mask_account_card(from_)
    masked_to = mask_account_card(to_)

    print(f"{formatted_date} {transaction['description']}")
    print(f"{masked_from} -> {masked_to}")
    print(f"Сумма: {amount:.2f} {currency_name}\n")


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    while True:
        user_input = input(prompt).strip().upper()
        if user_input in map(str.upper, valid_choices):
            return user_input
        else:
            print(f"Вариант '{user_input}' недоступен.")


def main():
    global current_transactions

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_type = get_user_choice("Ваш выбор: ", ["1", "2", "3"])

    # Загружаем данные
    if file_type == "1":
        print("\nДля обработки выбран JSON-файл.")
        current_transactions = load_json_file("./data/operations.json")
    elif file_type == "2":
        print("\nДля обработки выбран CSV-файл.")
        current_transactions = load_csv_file("./data/transactions.csv")
    elif file_type == "3":
        print("\nДля обработки выбран Excel-файл.")
        current_transactions = load_excel_file("./data/transactions_excel.xlsx")

    # Фильтрация по статусу
    allowed_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    status = get_user_choice(
        f"\nВведите статус, по которому необходимо выполнить фильтрацию.\nДоступные статусы: {' '.join(allowed_statuses)}\n",
        allowed_statuses,
    )
    filtered = list(filter_by_state(current_transactions, state=status))
    print(f'\nОперации отфильтрованы по статусу "{status}" ({len(filtered)} штук)')

    # Дополнительная фильтрация
    should_sort = get_user_choice(
        "\nОтсортировать операции по дате? Да/Нет\n", ["ДА", "НЕТ"]
    ).startswith("Д")

    if should_sort:
        order = get_user_choice(
            "\nОтсортировать по возрастанию или по убыванию?\n",
            ["ПО ВОЗРАСТАНИЮ", "ПО УБЫВАНИЮ"],
        )
        reverse = order.startswith("У")
        sorted_transactions = sort_by_date(filtered, reverse=reverse)
    else:
        sorted_transactions = filtered

    # Валюта
    only_rubles = get_user_choice(
        "\nВыводить только рублевые транзакции? Да/Нет\n", ["ДА", "НЕТ"]
    ).startswith("Д")

    if only_rubles:
        ruble_transactions = list(filter_by_currency(sorted_transactions, currency_code="RUB"))
    else:
        ruble_transactions = sorted_transactions

    # Поиск по описанию
    use_search = get_user_choice(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n",
        ["ДА", "НЕТ"],
    ).startswith("Д")

    if use_search:
        search_query = input("\nВведите ключевое слово для поиска: ").strip()
        final_result = search_by_description(ruble_transactions, search_query)
    else:
        final_result = ruble_transactions

    # Итог
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(final_result)}")

    if final_result:
        for trx in final_result[:5]:  # Выведем максимум 5 первых
            print_transaction(trx)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()
