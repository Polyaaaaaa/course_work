import re
import pandas as pd


def get_operations_dict(filepath: str) -> list:
    operations = pd.read_excel(filepath)
    file_dict = operations.to_dict(orient="records")
    return file_dict


def find_string(filepath: str, search_bar: str) -> list:
    """
    функция поиска операций с определенными словами в описании
    """
    result = []
    pattern = re.compile(search_bar, re.IGNORECASE)
    for operation in get_operations_dict(filepath):
        if pattern.search(search_bar):
            result.append(operation)
    return result


#print(
#   get_operations_dict(
#      "C:\\Users\\Kir\\PycharmProjects\\pythonProject\\data\\operations.xls")
#)
