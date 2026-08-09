import json
from typing import List, Dict

import logging

logger = logging.getLogger("utils")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs/utils.log", mode="w")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def load_json_file(file_path: str) -> List[Dict]:
    """
    Загружает данные из JSON-файла...
    """

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                logger.info(
                    f"Успешно прочитан файл операций: {file_path}"
                )  # <--- ДОБАВЬТЕ ЭТОТ ЛОГ
                return data
            else:
                logger.error(
                    f"Файл существует, но содержит неверные данные: {file_path}"
                )  # <--- И ЭТОТ
                return []

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")  # <--- И ЭТОТ
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}", exc_info=True)  # <--- И ЭТОТ
        return []
