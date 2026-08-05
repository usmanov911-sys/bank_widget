import json
from typing import List, Dict


def load_json_file(file_path: str) -> List[Dict]:
    """
    Загружает данные из JSON-файла и возвращает их как список словарей.

    Args:
        file_path (str): Путь к файлу JSON.

    Returns:
        List[Dict]: Список транзакций или пустой список,
                   если файл не найден, пуст или содержит неверные данные.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data
            else:
                return []

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
