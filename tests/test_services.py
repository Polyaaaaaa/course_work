from unittest.mock import Mock, patch, MagicMock
from src.services import get_operations_dict
import json
import os
import pandas as pd


# def test_get_operations_dict() -> None:
#     transactions = get_operations_dict("..\\data\\operations.xls")
#     assert transactions[1] == {
#         "Дата операции": "17.07.2019 15:01:15",
#         "Дата платежа": "19.07.2019",
#         "Номер карты": "*7197",
#         "Статус": "OK",
#         "Сумма операции": -27.0,
#         "Валюта операции": "RUB",
#         "Сумма платежа": -27.0,
#         "Валюта платежа": "RUB",
#         "Кэшбэк": nan,
#         "Категория": "Дом и ремонт",
#         "MCC": 5200.0,
#         "Описание": "OOO Nadezhda",
#         "Бонусы (включая кэшбэк)": 0,
#         "Округление на инвесткопилку": 0,
#         "Сумма операции с округлением": 27.0,
#     }


# def test_get_operations_dict() -> None:
#     # Мокируем функцию pd.read_excel
#     read_excel_mock = MagicMock(return_value=pd.DataFrame([{"Дата операции": "17.07.2019 15:01:15"}]))
#     pd.read_excel = read_excel_mock
#
#     transactions = get_operations_dict("..\\data\\operations.xls")
#     assert transactions[1] == {
#         "Дата операции": "17.07.2019 15:01:15",
#         "Дата платежа": "19.07.2019",
#         "Номер карты": "*7197",
#         "Статус": "OK",
#         "Сумма операции": -27.0,
#         "Валюта операции": "RUB",
#         "Сумма платежа": -27.0,
#         "Валюта платежа": "RUB",
#         "Кэшбэк": nan,
#         "Категория": "Дом и ремонт",
#         "MCC": 5200.0,
#         "Описание": "OOO Nadezhda",
#         "Бонусы (включая кэшбэк)": 0,
#         "Округление на инвесткопилку": 0,
#         "Сумма операции с округлением": 27.0,
#     }
