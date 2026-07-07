# Банковские операции

## Описание

Проект предназначен для обработки банковских операций.

Реализованы функции:

- фильтрация операций по статусу;
- сортировка операций по дате;
- маскирование банковских карт и счетов.

## Установка

Для установки зависимостей используется Poetry.

Установить зависимости:

```bash

poetry install
````

## Использование

Пример использования функций:

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2024-01-01"
    }
]

filtered = filter_by_state(operations)

sorted_operations = sort_by_date(filtered)
```
## Тестирование 
Для запуска тестов выполните команду:

```bash

pytest
```
## Автор

Artur