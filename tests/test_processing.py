import pytest
from src.processing import filter_by_state, sort_by_date


# ФИКСТУРА: создаём список транзакций один раз
@pytest.fixture
def transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03"}
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