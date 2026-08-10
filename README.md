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
- Новая функциональность: поддержка чтения данных из файлов разных форматов (JSON, CSV, XLSX) через модуль src/data_loader.
## Новая функциональность: работа с разными форматами данных
В рамках развития проекта реализована загрузка данных о транзакциях не только из JSON-файла, но и из табличных форматов.

Для этого создан отдельный модуль src/data_loader.py, который содержит функции:
- load_csv_file(file_path) — читает данные из файла формата .csv. Принимает путь к файлу как аргумент и возвращает список словарей.
- load_excel_file(file_path) — читает данные из файла формата .xlsx или .xls. Также принимает путь к файлу и возвращает список словарей.

Библиотеки pandas и openpyxl добавлены в зависимости проекта.
```
Примечание: примеры данных для работы с этими функциями можно найти в папке /data/:  
- transactions.csv  
- transactions_excel.xlsx
```
## Пример использования нового модуля:

```python
from src.data_loader import load_csv_file, load_excel_file

# Загрузка данных из CSV
csv_data = load_csv_file("./data/transactions.csv")
print(f"Загружено {len(csv_data)} записей из CSV.")

# Загрузка данных из Excel
excel_data = load_excel_file("./data/transactions_excel.xlsx")
print(f"Загружено {len(excel_data)} записей из Excel.")
```
(Обратите внимание, что структура данных во всех трёх случаях идентична — это список словарей, поэтому вы можете использовать одни и те же функции обработки независимо от источника). 
## Установка

Для установки зависимостей используется Poetry.

Установить зависимости:

```bash

poetry install
````
Запустите тесты:
```bash

pytest --cov=src --cov-report=html
```
Покрытие должно быть более 80%.

## Использование функций

Пример использования функций из модулей processing.py и generators.py:

```python
from src.processing import filter_by_state, sort_by_date
from src.generators import card_number_generator, transaction_descriptions, filter_by_currency
from src.data_loader import load_json_file, load_csv_file

# Загрузим данные из любого формата
json_data = load_json_file("./data/operations.json") # Старый способ
csv_data = load_csv_file("./data/transactions.csv") # Новый способ

# Объединяем все наборы данных
all_transactions = json_data + csv_data

# Отфильтруем только выполненные USD-транзакции
usd_executed = list(filter_by_state(
    filter_by_currency(all_transactions, currency_code="USD"),
    state="EXECUTED"
))
for operation in usd_executed[:3]:
    print(operation["description"])

# Получим описания первых двух операций
descriptions = transaction_descriptions(all_transactions)
print("Первые два описания:")
print(next(descriptions))  # "Перевод организации"
print(next(descriptions))  # "Пополнение счёта"

# Генерируем номера карт
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