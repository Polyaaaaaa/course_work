import os
import json
from heapq import nlargest

import pandas as pd
import requests
import logging
from typing import Sequence

from dotenv import load_dotenv

from src.services import get_operations_dict
from src.utils import get_card_num, get_top_of_transactions, hi_message

from datetime import datetime

load_dotenv()
API_KEY_1 = os.getenv("API_KEY_1")
API_KEY_2 = os.getenv("API_KEY_2")

logger = logging.getLogger("views")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_json_answer(date: str) -> Sequence[object] | str | None:
    """Функция, принимающая на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающая JSON-ответ со следующими данными:
    1. Приветствие
    2. По каждой карте: последние 4 цифры карты; общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей).
    3. Топ-5 транзакций по сумме платежа.
    4. Курс валют.
    5. Стоимость акций из S&P500."""
    logger.info("start home_page")
    card_numbers = []
    unique_cards = []
    big_amount = []
    top_transactions = []
    stock_prices = []
    currency_rates = []
    currency = ["USD", "EUR"]
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    output = {
        "greeting": "",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [Sequence[str]],
        "stock_prices": [],
    }

    time_format = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    morning = datetime.strptime("05:00:00", "%H:%M:%S")
    day = datetime.strptime("12:00:00", "%H:%M:%S")
    evening = datetime.strptime("18:00:00", "%H:%M:%S")
    night = datetime.strptime("23:00:00", "%H:%M:%S")
    if morning.time() <= time_format.time() < day.time():
        greet = "Доброе утро!"
    elif morning.time() <= time_format.time() < evening.time():
        greet = "Добрый день!"
    elif evening.time() <= time_format.time() < night.time():
        greet = "Добрый вечер!"
    else:
        greet = "Доброй ночи!"

    output["greeting"] = greet
    for item in currency:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY_1}/latest/{item}"
        response = requests.get(url, headers={"apikey": API_KEY_1})
        response_data = response.json()
        path = response_data.get("conversion_rates", {}).get("RUB")
        currency_rates.append(dict(currency=item, rate=path))
    output["currency_rates"] = currency_rates

    data = get_operations_dict("../data/operations.xls")
    for transaction in data:
        if not pd.isnull(transaction.get("Номер карты")):
            card_numbers.append(dict(last_digits=transaction.get("Номер карты", "").replace("*", "")))
    for card in card_numbers:
        if card not in unique_cards:
            unique_cards.append(card)
    for transaction in data:
        if not pd.isnull(transaction.get("Номер карты")):
            for unique in unique_cards:
                if unique.get("last_digits", "") in transaction.get("Номер карты", ""):
                    if pd.isnull(transaction.get("Сумма операции", "")) is False:
                        try:
                            unique["total_spent"] += abs(transaction.get("Сумма операции", ""))
                            unique["cashback"] += abs(transaction.get("Сумма операции", "") / 100)
                        except KeyError:
                            unique["total_spent"] = abs(transaction.get("Сумма операции", ""))
                            unique["cashback"] = abs(transaction.get("Сумма операции", "") / 100)
    for unique in unique_cards:
        unique["total_spent"] = round(float(unique.get("total_spent", "")), 2)
        unique["cashback"] = round(float(unique.get("cashback", "")), 2)
    output["cards"] = unique_cards

    for transaction in data:
        big_amount.append(transaction.get("Сумма операции"))
    big_amount = nlargest(5, big_amount)
    for transaction in data:
        for amount in big_amount:
            if transaction.get("Сумма операции") == amount:
                top_transactions.append(
                    dict(
                        date=transaction.get("Дата платежа"),
                        amount=amount,
                        category=transaction.get("Категория"),
                        description=transaction.get("Описание"),
                    )
                )
                big_amount.remove(amount)
    output["top_transactions"] = top_transactions

    url_2 = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY_2}"
    response_2 = requests.get(url_2, headers={"apikey": API_KEY_2})
    response_data_2 = response_2.json()
    for share in response_data_2:
        for stock in stocks:
            if share.get("symbol", "") == stock:
                stock_prices.append(dict(stock=stock, price=share.get("price", "")))
    output["stock_prices"] = stock_prices

    json_data = json.dumps(output, ensure_ascii=False, indent=4)
    logger.info(f"end home_page\n{json_data}\n")

    with open("user_settings.json", "w") as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    return json_data


print(get_json_answer("2021-12-31 16:39:04"))