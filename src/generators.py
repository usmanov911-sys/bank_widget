
def filter_by_currency(transactions, currency_code):
    """
    Эта функция ищет среди всех операций те, где валюта совпадает с нужной.

    Она возвращает не список, а специальный объект-итератор,
    который выдаёт результаты по одному.
    """
    return (
        transaction for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code
    )


def transaction_descriptions(transactions):
    """
    Эта функция берёт список операций и по очереди отдает их описания.
    """
    for operation in transactions:
        yield operation["description"]


def card_number_generator(start=1, stop=9_999_999_999_999_999):
    """
    Генерирует красивые банковские карты вида XXXX XXXX XXXX XXXX.

    start - номер первой карты (по умолчанию 1).
    stop - номер последней карты (включительно).
    """
    # Проходим по диапазону чисел
    for number in range(start, stop + 1):
        # Делаем красивую строку из числа
        formatted = f"{number:016d}"  # Добавляет нули слева
        parts = [formatted[i:i + 4] for i in range(0, 16, 4)]
        yield " ".join(parts)
