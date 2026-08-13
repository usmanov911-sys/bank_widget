from datetime import datetime
from typing import Any

import re
from typing import List, Dict
from collections import Counter


def filter_by_state(
    operations: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """
    Фильтрует операции по статусу.

    Args:
        operations: Список операций в виде словарей.
        state: Статус операции для фильтрации.

    Returns:
        Список операций с указанным статусом.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """
    Сортирует операции по дате.

    Args:
        operations: Список операций.
        reverse: Если True, новые операции будут выше старых.

    Returns:
        Отсортированный список операций.
    """
    return sorted(
        operations, key=lambda operation: datetime.fromisoformat(operation["date"]), reverse=reverse
    )


def search_by_description(transactions: List[Dict], query: str) -> List[Dict]:
    """
    Ищет операции, содержащие заданную строку в поле description.

    Args:
        transactions (List[Dict]): Список транзакций.
        query (str): Строка запроса для поиска.

    Returns:
        List[Dict]: Список операций, в описании которых найдено совпадение.
    """
    pattern = re.compile(query, flags=re.IGNORECASE)

    return [
        transaction
        for transaction in transactions
        if "description" in transaction and pattern.search(transaction["description"])
    ]


def count_operations_by_categories(transactions: List[Dict], categories: List[str]) -> dict:
    """
    Считает количество операций по указанным категориям.

    Категории ищутся в поле description каждой операции.

    Args:
        transactions (List[Dict]): Список транзакций.
        categories (List[str]): Список ключевых слов-категорий.

    Returns:
        dict: Словарь {категория: количество}.
    """
    counter = Counter()

    for transaction in transactions:
        desc = transaction.get("description", "").lower()

        for category in categories:
            if category.lower() in desc:
                counter[category] += 1

    return dict(counter)
