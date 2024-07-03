import requests
from datetime import datetime
import logging
import pandas
import json
from utils import hi_message, mask_by_card_number, add_to_json_file
from src.services import get_operations_dict

logger = logging.getLogger("views")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main_page(date: str, transactions: list[dict]) -> str:
    """Главная функция для отображения главной страницы"""
    logger.info("Запустили главную страницу")
    greeting = hi_message(date)
    cards = mask_by_card_number(transactions)
    result = {"greeting": greeting, "cards": cards}
    add_to_json_file("user_settings.json", result)
    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    logger.info("Запуск веб-страниц")
    transactions = get_operations_dict("..\\data\\operations.xls")
    user_date = input("Введите пожалуйста вашу дату в таком формате: 'DD:MM:YYYY HH:MM:SS'")
    add_to_json_file(date=user_date, transactions=transactions)





