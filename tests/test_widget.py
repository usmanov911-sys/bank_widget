import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Classic 1234567890123456", "Visa Classic **** **** **** 3456"),  # Карта
        ("Счёт 12345678901234567890", "Счёт **XXXX XXXX XXXX XXXX XX90"),  # Счёт
        ("Некорректные данные", None),  # Некорректный ввод
    ]
)
def test_mask_account_card(input_data, expected):
    """Тестирование универсальной маски для счёта/карты"""
    result = mask_account_card(input_data)
    assert result == expected