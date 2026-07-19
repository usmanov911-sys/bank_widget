
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

