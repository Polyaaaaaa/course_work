import json
import logging
import re

import pandas as pd

# import os

logger = logging.getLogger("services")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_operations_dict(filepath: str) -> list:
    """функция, возращающая список словарей из ексель файла"""
    logger.info(f"start get_operations_dict {filepath}")

    operations = pd.read_excel(filepath)
    operations = operations.where(pd.notnull(operations), None)
    file_dict = operations.to_dict(orient="records")

    logger.info("Файл прочтён корректно")

    return file_dict


def find_string(filepath: str, search_bar: str) -> str:
    """
    функция поиска операций с определенными словами в описании
    """
    logger.info("start find_string ")

    df = filepath
    result = []
    pattern = re.compile(search_bar, re.IGNORECASE)
    for operation in get_operations_dict(df):
        if pattern.search(str(operation["Категория"])):
            result.append(operation)

    logger.info("Список транзакций отсортирован по искомой строке")

    data = json.dumps(result, ensure_ascii=False)
    return data


# print(find_string(os.path.join("..", "data", "operations.xls"), "Переводы"))
# print(get_operations_dict(os.path.join("..", "data", "operations.xls"))
