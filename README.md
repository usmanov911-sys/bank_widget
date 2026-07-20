# Банковские операции

## Описание проекта

Проект предназначен для обработки банковских операций. Он предоставляет инструменты для фильтрации, сортировки данных, а также для генерации тестовых наборов информации.

Реализованы модули и функционал:

- фильтрация операций по статусу (filter_by_state);
- сортировка операций по дате (sort_by_date);
- маскирование банковских карт и счетов.
- новые генераторы для эффективной работы с данными:
  - Фильтр транзакций по валюте — filter_by_currency()
  - Генерация описаний операций — transaction_descriptions()
  - Генерация номеров банковских карт — card_number_generator(start=..., stop=...)
## Установка

Для установки зависимостей используется Poetry.

Установить зависимости:

```bash

poetry install
````

## Использование функций

Пример использования функций из модулей processing.py и generators.py:

```python
from src.processing import filter_by_state, sort_by_date
from src.generators import card_number_generator, transaction_descriptions, filter_by_currency

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD"}},
        "description": "Перевод организации"
    },
    # ... другие операции ...
]

# Старый функционал + Генератор №1: отфильтруем только выполненные USD-транзакции
usd_executed = filter_by_state(list(filter_by_currency(transactions, currency_code="USD")))
for operation in usd_executed:
    print(f"Операция {operation['id']} выполнена.")

# Новый функционал №2: получим описания первых двух операций
descriptions = transaction_descriptions(transactions)
print("Первые два описания:")
print(next(descriptions))
print(next(descriptions))

# Новый функционал №3: генерируем номера карт
print("\nПять случайных номеров карт:")
for number in card_number_generator(1_000_000, 1_000_005):  
    print(number)  # Выведет пять красивых номеров карт
```
## Тестирование 
Для запуска тестов выполните команду:

```bash

pytest
```
## Автор

Artur