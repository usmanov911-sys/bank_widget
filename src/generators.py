
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