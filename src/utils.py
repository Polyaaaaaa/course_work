import json
import logging
from datetime import datetime

import requests

# import pandas as pd
# import os

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
    current_date = datetime.strptime(date, "%Y.%m.%d %H:%M:%S").time()

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
    if card_number is None:
        pass
    else:
        return card_number[-4:]


def get_cashback(total_expenses: float) -> float:
    """Возвращает сумму кешбэка по общим расходам"""
    return total_expenses / 100


def get_top_of_transactions(transactions: list) -> list:
    """Возвращает список из n транзакций с наибольшей суммой платежа"""
    # sums = []
    # for transaction in transactions:
    #     sums.append(transaction["Сумма платежа"])

    sorted_list = sorted(transactions, key=lambda x: x['Сумма платежа'])[-5::1]
    return sorted_list


# def get_currency_rates() -> json | str:
#     """функция, возращающая валюту и её цену за единицу этой валюты"""
#     url = "https://api.apilayer.com/currency_data/live"
#     params = {"base": "RUB", "symbols": "EUR,USD"}
#     headers = {"apikey": "FZ3ahVSsZCDfaRFeuyZdRoIyOrzAzavs"}
#
#     response = requests.get(url, params=params, headers=headers)
#
#     if response.status_code == 200:
#         data = response.json()
#         rates = data.get("rates", {})
#         currency_rates = [
#             {"currency": "USD", "rate": int(rates.get("USD", 0))},
#             {"currency": "EUR", "rate": int(rates.get("EUR", 0))},
#         ]
#         return json.dumps({"currency_rates": currency_rates})
#     else:
#         # return f"Ошибка: {response.status_code}"
#         return "Ошибка"


# def get_stock_prices() -> str:
#     """функция, возращающая акции и их стоимость"""
#     url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,AMZN,GOOGL,MSFT,TSLA"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()["quoteResponse"]["result"]
#         stock_prices = []
#         for stock in data:
#             stock_prices.append({"stock": stock["symbol"], "price": stock["regularMarketPrice"]})
#         return json.dumps({"stock_prices": stock_prices})
#     else:
#         # return f"Ошибка: {response.status_code}"
#         return "Ошибка"


# print(hi_message("2024:07:03 22:00:00"))
# print(get_sum_of_transactions("..\\data\\operations.xls"))
# print(get_currency_rates())
# print(get_stock_prices())
# print(get_cashback(14645427.39))
# print(get_top_of_transactions(get_operations_dict("..\\data\\operations.xls")))
