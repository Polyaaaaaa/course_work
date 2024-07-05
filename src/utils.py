from datetime import datetime
import logging
from src.services import get_operations_dict
import requests
import json

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def hi_message(date: str) -> str | None:
    """Функция, возращающая приветствие в зависимости от времени"""

    logger.info("Анализируем, какое приветствие выбрать")
    current_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S").time()

    if 5 <= current_date.hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= current_date.hour < 17:
        greeting = "Добрый день!"
    elif 17 <= current_date.hour < 23:
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"

    logger.info(f"Приветствие будет: {greeting}")

    return greeting


def get_card_num(card_number: str) -> str:
    """Возвращает последние 4 цифры номера карты"""
    return card_number[-4:]


def get_sum_of_transactions(filepath: str) -> float:
    """Возвращает общую сумму расходов по транзакциям"""
    transactions = get_operations_dict(filepath)
    sums = []

    for element in transactions:
        if element["Категория"] == "Пополнения":
            pass
        else:
            if element["Сумма платежа"] < 0:
                sums.append(element["Сумма платежа"] * -1)
            else:
                sums.append(element["Сумма платежа"])

    return sum(sums)


def get_cashback(total_expenses: float) -> float:
    """Возвращает сумму кешбэка по общим расходам"""
    return total_expenses / 100


def get_top_of_transactions(transactions: list) -> list:
    """Возвращает список из n транзакций с наибольшей суммой платежа"""
    sums = []
    for transaction in transactions:
        sums.append(transaction["Сумма платежа"])
    return list(sorted(sums)[-5::1])


def get_currency_rates():
    """функция, возращающая валюту и её цену за единицу этой валюты"""
    url = "https://api.apilayer.com/currency_data/live"
    params = {
        "base": "RUB",
        "symbols": "EUR,USD"
    }
    headers = {
        "apikey": "Y0NJSYiThQhh4r2ykGqyoeHJ8OISMbYU"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        rates = data.get("rates", {})
        currency_rates = [
            {
                "currency": "USD",
                "rate": int(rates.get("USD", 0))
            },
            {
                "currency": "EUR",
                "rate": int(rates.get("EUR", 0))
            }
        ]
        return json.dumps({"currency_rates": currency_rates})
    else:
        return f"Ошибка: {response.status_code}"


def get_stock_prices():
    """функция, возращающая акции и их стоимость"""
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,AMZN,GOOGL,MSFT,TSLA"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["quoteResponse"]["result"]
        stock_prices = []
        for stock in data:
            stock_prices.append({
                "stock": stock["symbol"],
                "price": stock["regularMarketPrice"]
            })
        return json.dumps({"stock_prices": stock_prices})
    else:
        return f"Ошибка: {response.status_code}"


def add_to_json_file(stock_prices, currency_rates, top_five, cashback, summ, card_num):




#print(hi_message("2024:07:03 22:00:00"))
#print(get_sum_of_transactions("..\\data\\operations.xls"))
#print(get_currency_rates())
print(get_stock_prices())
