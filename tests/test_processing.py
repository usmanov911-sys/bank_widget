import pytest
from src.processing import filter_by_state, sort_by_date

from src.processing import search_by_description


@pytest.fixture
def transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03"},
    ]


def test_filter_by_state(transactions):
    """Тест фильтрации по статусу EXECUTED"""
    filtered = filter_by_state(transactions, state="EXECUTED")
    assert len(filtered) == 2
    for transaction in filtered:
        assert transaction["state"] == "EXECUTED"


def test_sort_by_date_descending(transactions):
    """Тест сортировки по дате в обратном порядке"""
    sorted_transactions = sort_by_date(transactions, reverse=True)
    dates = [t["date"] for t in sorted_transactions]
    assert dates == ["2023-01-03", "2023-01-02", "2023-01-01"]


@pytest.fixture(scope="session")
def sample_data():
    """Возвращает список транзакций для тестирования."""
    return [
        {"id": 1, "description": "Оплата товаров"},
        {"id": 2, "description": "Перечисление зарплаты"},
        {"id": 3, "description": "Покупка авиабилетов"},
        {"id": 4},
    ]


def test_search_by_description(sample_data):
    result = search_by_description(sample_data, r"оплат|перечислен|авиабилетов")
    assert len(result) == 3
    assert set(t["id"] for t in result) >= {1, 2}


def test_search_case_insensitive(sample_data):
    result = search_by_description(sample_data, r"товары?")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_search_no_match(sample_data):
    result = search_by_description(sample_data, r"отпуск")
    assert not result
