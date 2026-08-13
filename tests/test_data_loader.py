import pytest
from unittest.mock import patch
from src.data_loader import load_csv_file, load_excel_file


@pytest.fixture(scope="session")
def csv_sample() -> dict:
    """
    Возвращает структуру одной записи из transactions.csv.
    """
    return {
        "id": "67951f02-cb9c-495d-bae9-0f3e1cbd66ed",
        "state": "EXECUTED",
        "date": "2019-07-13T18:41:22.334068",
    }


@patch("pandas.read_csv")
def test_load_csv(mock_read_csv, csv_sample):
    """Тестируем загрузку CSV."""

    mock_df = mock_read_csv.return_value
    mock_df.to_dict.return_value = [csv_sample]
    result = load_csv_file("./fake/path/to/file.csv")

    # Проверяем, что функция была вызвана правильно
    mock_read_csv.assert_called_once_with("./fake/path/to/file.csv", sep=",", header=0, dtype=str)

    assert len(result) > 0, "CSV-файл не прочитан"
    first_record = result[0]

    for key in csv_sample.keys():
        assert key in first_record, f"Ключ '{key}' отсутствует в первой записи транзакции."


@patch("pandas.read_excel")
def test_load_excel(mock_read_excel, csv_sample):
    """Тестируем загрузку Excel."""

    mock_df = mock_read_excel.return_value
    mock_df.to_dict.return_value = [csv_sample]

    result = load_excel_file("./fake/path/to/excel.xlsx")

    mock_read_excel.assert_called_once_with("./fake/path/to/excel.xlsx", sheet_name=0, dtype=str)

    assert len(result) > 0, "Excel-файл не прочитан"
    first_record = result[0]

    for key in csv_sample.keys():
        assert key in first_record, f"Ключ '{key}' отсутствует в первой записи транзакции."
