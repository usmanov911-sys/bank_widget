import pytest
from unittest.mock import patch
from src.external_api import convert_to_rubles


@pytest.fixture
def sample_transaction_usd():
    """Транзакция в долларах."""
    return {
        "id": 1,
        "state": "EXECUTED",
        "date": "2023-07-01T12:00:00",
        "operationAmount": {"amount": "100.50", "currency": {"name": "USD", "code": "USD"}},
    }


@patch("requests.get")
def test_convert_usd(mock_get, sample_transaction_usd):
    mock_response = mock_get.return_value
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 100.5},
        "result": 9045.00,
    }

    result = convert_to_rubles(sample_transaction_usd, commission_rate=0)
    assert round(result, 2) == 9045.00


@patch("requests.get")
def test_convert_eur(mock_get):
    pass
