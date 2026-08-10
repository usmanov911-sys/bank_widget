import pandas as pd
from typing import List, Dict

import logging

logger = logging.getLogger()


def load_csv_file(file_path: str) -> List[Dict]:
    """
    Загружает данные о транзакциях из файла CSV.

    Args:
        file_path (str): Путь к файлу CSV.

    Returns:
        List[Dict]: Список словарей с данными или пустой список при ошибке.
    """

    try:
        # Читаем CSV-файл через pandas
        df = pd.read_csv(
            file_path,
            sep=",",  # Разделитель столбцов
            header=0,  # Первая строка — заголовки колонок
            dtype=str,  # Все колонки читаем как строки
        )

        # Конвертируем табличные данные обратно в тот же формат списка словарей
        return df.to_dict(orient="records")

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден!")
        return []

    except Exception as e:
        logger.error(f"Ошибка чтения CSV ({e})", exc_info=True)
        return []


def load_excel_file(file_path: str) -> List[Dict]:
    """
    Загружает данные о транзакциях из файла Excel (*.xls или *.xlsx).

    Args:
        file_path (str): Путь к файлу Excel.

    Returns:
        List[Dict]: Список словарей с данными или пустой список при ошибке.
    """

    try:
        # Pandas сам определяет формат (xls/xlsx), если передать путь
        df = pd.read_excel(
            file_path, sheet_name=0, dtype=str  # Читаем первый лист  # Все колонки как строки
        )

        return df.to_dict(orient="records")

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден!")
        return []

    except Exception as e:
        logger.error(f"Ошибка чтения Excel ({e})", exc_info=True)
        return []
