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
## Модуль decorators

В рамках выполнения домашнего задания добавлен новый модуль src/decorators.py, содержащий универсальный декоратор @log.

### Назначение модуля:
Декоратор предназначен для автоматического логирования работы функций. Он позволяет отслеживать выполнение кода без необходимости вручную добавлять вызовы print() или записи в файл внутри каждой функции.

### Функциональность декоратора:
- Логирует время начала и окончания вызова функции.
- Записывает имя функции (__name__), её аргументы (args, kwargs) и результат выполнения (или ошибку).
- Поддерживает два режима вывода:  
1. В консоль (по умолчанию) — если аргумент filename=None.  
2. В указанный файл — если передан путь к файлу через параметр filename="имя_файла.txt".
## Формат логов:
```
[YYYY-MM-DD HH:mm:ss] полное_имя_функции started
[YYYY-MM-DD HH:mm:ss] полное_имя_функции ok
```
### Или при ошибке:
```
[YYYY-MM-DD HH:mm:ss] полное_имя_функции error: TypeError. Inputs: args=(10,), kwargs={}
```
## Пример использования:
```python
# Импортируем декоратор из нового модуля
from src.decorators import log

# Вариант А: вывод в консоль (аргумент filename опущен)
@log()
def calculate_discount(price: float, discount: int):
    return price - (price * discount / 100)

result = calculate_discount(500, 10)
# Вывод в консоль будет примерно таким:
# [2026-07-30 14:59:12] test_decorators.calculate_discount started
# [2026-07-30 14:59:12] test_decorators.calculate_discount ok

# Вариант Б: запись в файл
@log(filename="app.log")
def process_data(data: list[int]) -> None:
    for item in data:
        print(item)

process_data([1, 2, 3])
# Результат будет записан в файл app.log
```
## Тестирование 
Для запуска тестов выполните команду:

```bash

pytest
```
## Автор

Artur