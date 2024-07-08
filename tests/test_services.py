import unittest.mock
from unittest.mock import Mock, patch
from src.services import get_operations_dict, find_string
import json
import os
import pandas as pd


@patch("pandas.read_excel", create=True)
def test_get_list_of_transactions(mock_read_excel: Mock) -> None:
    mock_read_excel.return_value = pd.DataFrame(
        {
            "Дата операции": ["16.07.2019 16:30:10"],
            "Дата платежа": ["18.07.2019"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-49.8],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-49.8],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [None],
            "Категория": ["Супермаркеты"],
            "MCC": [5411.0],
            "Описание": ["SPAR"],
            "Бонусы (включая кэшбэк)": [0],
            "Округление на инвесткопилку": [0],
            "Сумма операции с округлением": [49.8],
        }

    )
    result = get_operations_dict("..\\data\\operations.xls")
    expected = [
        {
            "Дата операции": "16.07.2019 16:30:10",
            "Дата платежа": "18.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -49.8,
            "Валюта операции": "RUB",
            "Сумма платежа": -49.8,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "SPAR",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 49.8,
        }
    ]

    assert result == expected


@patch('builtins.open', create=True)
def test_find_string(mock_open):
    mock_file = mock_open()
    mock_file.return_value.__enter__.return_value = json.dumps([
        {'Категория': 'Еда', 'Сумма операции': -100, 'Описание': 'Магазин'},
        {'Категория': 'Транспорт', 'Сумма операции': -50, 'Описание': 'АЗС'},
        {'Категория': 'Еда', 'Сумма операции': -200, 'Описание': 'Ресторан'}
    ])

    result = find_string('..\\data\\operations.xls', 'еда')

    expected_result = [
        {'Категория': 'Еда', 'Сумма операции': -100, 'Описание': 'Магазин'},
        {'Категория': 'Еда', 'Сумма операции': -200, 'Описание': 'Ресторан'}
    ]
    assert json.loads(result) == expected_result
    mock_open.assert_called_once_with('..\\data\\operations.xls', 'r', encoding='utf-8')
