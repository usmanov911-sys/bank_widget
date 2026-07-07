from datetime import datetime
from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]],
    state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """
    Фильтрует операции по статусу.

    Args:
        operations: Список операций в виде словарей.
        state: Статус операции для фильтрации.

    Returns:
        Список операций с указанным статусом.
    """
    return [
        operation
        for operation in operations
        if operation.get("state") == state
    ]


def sort_by_date(
    operations: list[dict[str, Any]],
    reverse: bool = True
) -> list[dict[str, Any]]:
    """
    Сортирует операции по дате.

    Args:
        operations: Список операций.
        reverse: Если True, новые операции будут выше старых.

    Returns:
        Отсортированный список операций.
    """
    return sorted(
        operations,
        key=lambda operation: datetime.fromisoformat(operation["date"]),
        reverse=reverse
    )