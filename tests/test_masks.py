import pytest

from src.masks import get_mask_card_number, get_mask_account

# Тесты для get_mask_card_number

def test_get_mask_card_number_correct():
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"


def test_get_mask_card_number_invalid_length_short():
    with pytest.raises(ValueError):
        get_mask_card_number("12345678")


def test_get_mask_card_number_invalid_length_long():
    with pytest.raises(ValueError):
        get_mask_card_number("12345678123456789")


# Тесты для get_mask_account

def test_get_mask_account_correct():
    assert get_mask_account("1234567890") == "**7890"


def test_get_mask_account_exactly_four_digits():
    assert get_mask_account("1234") == "**1234"


def test_get_mask_account_too_short():
    with pytest.raises(ValueError):
        get_mask_account("123")