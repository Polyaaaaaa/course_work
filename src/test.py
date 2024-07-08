import os
import json
import pandas as pd
import requests
import logging
from typing import Sequence

from dotenv import load_dotenv

from src.services import get_operations_dict
from src.utils import get_card_num, get_top_of_transactions, hi_message

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
    """
    Функция, возвращающая json-ответ
    """
    logger.info("start get_json_answer()")

    operations = get_operations_dict(os.path.join("..", "data", "operations.xls"))

    greeting = hi_message(date)

    cards = []
    special_cards = []
    top_transactions = []
    currency_rates_lst = []
    stock_prices_lst = []

    out_put_func = {
        "greeting": "",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": [],
    }
    currency = ["USD", "EUR"]
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    for element in currency:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY_1}/latest/{element}"
        response = requests.get(url, headers={"apikey": API_KEY_1})
        response_data = response.json()
        path = response_data.get("conversion_rates", {}).get("RUB")
        currency_rates_lst.append(dict(currency=element, rate=path))

    out_put_func["currency_rates"] = currency_rates_lst

    second_url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey=6f2HzBpYjOsKrtToEw4ClUylkGcM0YdN"
    second_response = requests.get(second_url, headers={"apikey": API_KEY_2})
    second_response_data = second_response.json()

    for info in second_response_data:
        for stock in stocks:
            if info.get("symbol", "") == stock:
                stock_prices_lst.append(dict(stock=stock, price=info.get("price", "")))

    top_five = get_top_of_transactions(operations)

    with open("user_settings.json", "a", encoding="utf-8") as file:
        for transaction in operations:
            card_num = get_card_num(transaction.get("Номер карты", ""))

            if not pd.isnull(card_num):
                cards.append(dict(last_digits=card_num, total_spent=0, cashback=0))

            for card in cards:
                if card.get("last_digits", "") == card_num:
                    if pd.isnull(transaction.get("Сумма операции", "")) is False:
                        card["total_spent"] += transaction.get("Сумма операции", "")
                        card["cashback"] += transaction.get("Сумма операции", "") / 100

            for card in cards:
                if card not in special_cards:
                    special_cards.append(card)

        for special in special_cards:
            special["total_spent"] = round(float(special.get("total_spent", "")))
            special["cashback"] = round(float(special.get("cashback", "")))
        out_put_func["cards"] = special_cards

        for element in top_five:
            if element.get("Сумма операции"):
                top_transactions.append(
                    dict(
                        date=element.get("Дата платежа"),
                        amount=element.get("Сумма операции"),
                        category=element.get("Категория"),
                        description=element.get("Описание"),
                    )
                )
                top_five.remove(element)
        out_put_func["top_transactions"] = top_transactions

        out_put_func["stock_prices"] = stock_prices_lst

        out_put_func["greeting"] = greeting

        json_answer = json.dumps(out_put_func, ensure_ascii=False, indent=4)

        logger.info("end of get_json_answer()")

        file.write(json_answer)

        return json_answer


print(get_json_answer("2021.12.31 16:39:04"))