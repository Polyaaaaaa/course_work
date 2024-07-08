import json
import logging
import os
from typing import Sequence

import pandas as pd
import requests
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

    with open("user_settings.json", "a", encoding="utf-8") as file:
        for transaction in operations:
            card_num = get_card_num(transaction.get("Номер карты", ""))
            greeting = hi_message(date)

            cards = []
            special_cards = []
            top_transactions = []
            currency_rates_lst = []
            stock_prices_lst = []

            top_five = get_top_of_transactions(operations)
            currency = ["USD", "EUR"]
            stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
            out_put_func = {
                "greeting": "",
                "cards": [],
                "top_transactions": [],
                "currency_rates": [Sequence[str]],
                "stock_prices": [],
            }

            for element in currency:
                url = f"https://v6.exchangerate-api.com/v6/{API_KEY_1}/latest/{element}"
                response = requests.get(url, headers={"apikey": API_KEY_1})
                response_data = response.json()
                path = response_data.get("conversion_rates", {}).get("RUB")
                currency_rates_lst.append(dict(currency=element, rate=path))
            out_put_func["currency_rates"] = currency_rates_lst

            if not pd.isnull(card_num):
                cards.append(dict(last_digits=card_num))

            for card in cards:
                if card not in special_cards:
                    special_cards.append(card)

            if not pd.isnull(card_num):
                for special in special_cards:
                    if special.get("last_digits", "") in card_num:
                        if pd.isnull(transaction.get("Сумма операции", "")) is False:
                            try:
                                special["total_spent"] += transaction.get("Сумма операции", "")
                                special["cashback"] += transaction.get("Сумма операции", "") / 100
                            except KeyError:
                                special["total_spent"] = transaction.get("Сумма операции", "")
                                special["cashback"] = transaction.get("Сумма операции", "") / 100

            for special in special_cards:
                special["total_spent"] = str(round(float(special.get("total_spent", "")), 2))
                special["cashback"] = str(round(float(special.get("cashback", "")), 2))

            out_put_func["cards"] = special_cards

            for element in top_five:
                if transaction.get("Сумма операции") == element:
                    top_transactions.append(
                        dict(
                            date=transaction.get("Дата платежа"),
                            amount=element,
                            category=transaction.get("Категория"),
                            description=transaction.get("Описание"),
                        )
                    )
                    top_five.remove(element)

            out_put_func["top_transactions"] = top_transactions

            second_url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey=6f2HzBpYjOsKrtToEw4ClUylkGcM0YdN"
            second_response = requests.get(second_url, headers={"apikey": API_KEY_2})
            second_response_data = second_response.json()

        for info in second_response_data:
            for stock in stocks:
                if info.get("symbol", "") == stock:
                    stock_prices_lst.append(dict(stock=stock, price=info.get("price", "")))

            out_put_func["stock_prices"] = stock_prices_lst

            out_put_func["greeting"] = greeting

            json_answer = json.dumps(out_put_func, ensure_ascii=False, indent=4)

            logger.info("end of get_json_answer()")

        file.write(json_answer)

        return json_answer


print(get_json_answer("2024.07.03 22:00:00"))
