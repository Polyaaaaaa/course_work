from datetime import datetime
import logging
from src.services import get_operations_dict
import requests
import json
import pandas as pd
import os
# from dotenv import load_dotenv


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

    url = "https://apilayer.com/marketplace/currency_data-api"

    load_dotenv()
    api_key = os.getenv("API_KEY")
    headers = {"apikey": api_key}
    payload: dict = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json().get("result", 0.0)

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
    params = {"base": "RUB", "symbols": "EUR,USD"}
    headers = {"apikey": "Y0NJSYiThQhh4r2ykGqyoeHJ8OISMbYU"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        rates = data.get("rates", {})
        currency_rates = [
            {"currency": "USD", "rate": int(rates.get("USD", 0))},
            {"currency": "EUR", "rate": int(rates.get("EUR", 0))},
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
            stock_prices.append({"stock": stock["symbol"], "price": stock["regularMarketPrice"]})
        return json.dumps({"stock_prices": stock_prices})
    else:
        return f"Ошибка: {response.status_code}"


def add_to_json_file(filepath):
    transactions = get_operations_dict(filepath)
    with open("user_settings.json", "a", encoding="utf-8") as file:
        for transaction in transactions:
            card_num = get_card_num(transaction["Номер карты"])
            date = transaction["Дата операции"]
            total_sum = get_sum_of_transactions("..\\data\\operations.xls")
            sum_of_payment = transaction["Сумма операции"]
            category = transaction["Категория"]
            description = transaction["Описание"]
            currency_rates = get_currency_rates()
            stock_prices = get_stock_prices()

            file.write(
                json.dumps(
                    {
                        {"greeting": hi_message(date)},
                        {
                            "cards": {
                                "last_digits": get_card_num(card_num),
                                "total_spent": total_sum,
                                "cashback": get_cashback(total_sum),
                            }
                        },
                        {
                            "top_transactions": {
                                "date": date,
                                "amount": sum_of_payment,
                                "category": category,
                                "description": description,
                            }
                        },
                        {"currency_rates": {currency_rates}},
                        {"stock_prices": stock_prices},
                    }
                )
            )


# print(hi_message("2024:07:03 22:00:00"))
# print(get_sum_of_transactions("..\\data\\operations.xls"))
print(get_currency_rates())
# print(get_stock_prices())
# print(add_to_json_file("..\\data\\operations.xls"))
# print(get_cashback(14645427.39))
# print(get_top_of_transactions(get_operations_dict("..\\data\\operations.xls")))
