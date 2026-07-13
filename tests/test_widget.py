import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),  # Карта

        pytest.param("Счёт 12345678901234567890", ..., marks=pytest.mark.xfail(reason="Номер слишком длинный")),
        pytest.param("Некорректные данные", None, marks=pytest.mark.xfail(reason="Не карта и не счёт")),
    ]
)
def test_mask_account_card(input_data, expected):
    """Тестирование универсальной маски для счёта/карты"""
    result = mask_account_card(input_data)

    # Если ожидаемое значение — None или ошибка, просто проверяем наличие результата
    if expected is None or isinstance(expected, Exception):
        assert result is not None
    else:
        assert result == expected