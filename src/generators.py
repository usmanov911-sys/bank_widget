def filter_by_currency(transactions: list[dict], currency_code: str):
    """
    Возвращает итератор операций с заданной валютой.
    При передаче None или пустой строки должен возвращать пустой итератор.
    """
    if not currency_code or currency_code is None:
        # Специальный случай: если валюту не указали,
        # мы должны вернуть пустой генератор.
        return iter([])

    return (
        t
        for t in transactions
        if t.get("operationAmount", {}).get("currency", {}).get("code") == currency_code
    )


def transaction_descriptions(transactions: list[dict]):
    """
    Генерирует описания операций по очереди.
    Пропускает операции, у которых нет поля description.
    """
    for op in transactions:
        # Используем get(), чтобы избежать ошибки KeyError
        desc = op.get("description")
        if desc is not None:
            yield desc


def card_number_generator(start=1, stop=9_999_999_999_999_999):
    """
    Генерирует красивые банковские карты вида XXXX XXXX XXXX XXXX.

    start - номер первой карты (по умолчанию 1).
    stop - номер последней карты (включительно).
    """
    # Проходим по диапазону чисел
    for number in range(start, stop):
        # Делаем красивую строку из числа
        formatted = f"{number:016d}"  # Добавляет нули слева
        parts = [formatted[i : i + 4] for i in range(0, 16, 4)]
        yield " ".join(parts)
