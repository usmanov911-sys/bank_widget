
import pytest
from src.generators import filter_by_currency

@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 3},  # Нет валюты вообще
        {"id": 4, "operationAmount": {"currency": {}}},  # Пустая валюта
    ]


@pytest.mark.parametrize(
    ["currency", "expected_ids"],
    [
        ("USD", [1]),          # Должна найти одну операцию
        ("RUB", [2]),
        ("EUR", []),           # Валюта отсутствует
        (None, []),            # Некорректный ввод тоже должен пройти нормально
    ],
)
def test_filter_by_currency(sample_transactions, currency, expected_ids):
    # Преобразуем итератор в список, чтобы можно было сравнить
    filtered = list(filter_by_currency(sample_transactions, currency))
    actual_ids = [t["id"] for t in filtered]
    assert sorted(actual_ids) == sorted(expected_ids)



from src.generators import transaction_descriptions

@pytest.fixture
def desc_transactions():
    return [
        {"description": "Операция 1"},
        {"description": "Операция 2"},
        {},  # Здесь описания нет!
    ]

def test_transaction_descriptions(desc_transactions):
    gen = transaction_descriptions(desc_transactions)
    # Берем первые два элемента
    assert next(gen) == "Операция 1"
    assert next(gen) == "Операция 2"
    # Третий элемент вызвать нельзя, т.к. описания нет -> ошибка StopIteration
    with pytest.raises(StopIteration):
        next(gen)



from src.generators import card_number_generator

def test_card_number_generator():
    cards = list(card_number_generator(1, 5))  # Сгенерируем пять первых карт
    assert cards == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ], "Формат неправильный!"

    # Проверим крайние значения
    first = next(card_number_generator())
    last = next(card_number_generator(stop=9_999_999_999_999_999))
    assert first == "0000 0000 0000 0001"
    assert last == "9999 9999 9999 9999"