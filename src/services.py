import re
import pandas as pd
import logging

logger = logging.getLogger("services")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_operations_dict(filepath: str) -> list:
    logger.info(f"start get_operations_dict {filepath}")

    operations = pd.read_excel(filepath)
    operations = operations.where(pd.notnull(operations), None)
    file_dict = operations.to_dict(orient="records")
    result = file_dict

    logger.info(f"the resulting list {result}")

    return result


def find_string(filepath: str, search_bar: str) -> list:
    """
    функция поиска операций с определенными словами в описании
    """
    logger.info(f"start find_string {filepath}, {search_bar}")

    df = filepath
    result = []
    pattern = re.compile(search_bar, re.IGNORECASE)
    for operation in get_operations_dict(df):
        if pattern.search(str(operation["Категория"])):
            result.append(operation)

    finish_result = result
    logger.info(f"the resulting list {finish_result}")

    return finish_result


print(find_string("..\\data\\operations.xls", "Переводы"))
