from src.utils import get_card_num, get_cashback, get_sum_of_transactions
from src.utils import get_stock_prices, get_currency_rates, get_operations_dict
from src.utils import get_top_of_transactions, hi_message
from unittest.mock import patch


# хорошо сделан, не нужно переделывать
def test_get_card_num() -> None:
    assert get_card_num("*7197") == "7197"


def test_get_sum_of_transactions() -> None:
    mock_transactions = [
        {"Категория": "Расходы", "Сумма платежа": -100},
        {"Категория": "Расходы", "Сумма платежа": -200},
        {"Категория": "Пополнения", "Сумма платежа": 300},
    ]
    with patch("utils.get_operations_dict", return_value=mock_transactions):
        assert get_sum_of_transactions(
            "C:\\Users\\Kir\\PycharmProjects\\pythonProject\\data\\operations.xls") == 300


# хорошо сделан, не нужно переделывать
def test_get_cashback() -> None:
    assert get_cashback(14645427.39) == 146454.2739


# хорошо сделан, не нужно переделывать
def test_hi_message() -> None:
    assert hi_message("2024:07:03 06:00:00") == "Доброе утро!"
    assert hi_message("2024:07:03 13:00:00") == "Добрый день!"
    assert hi_message("2024:07:03 18:00:00") == "Добрый вечер!"
    assert hi_message("2024:07:03 23:00:00") == "Доброй ночи!"


def test_get_top_of_transactions() -> None:
    mock_transactions = [
        {"Сумма платежа": -100},
        {"Сумма платежа": -200},
        {"Сумма платежа": -300},
        {"Сумма платежа": -400},
        {"Сумма платежа": -500},
        {"Сумма платежа": -600},
    ]
    with patch("services.get_operations_dict", return_value=mock_transactions):
        assert get_top_of_transactions(mock_transactions) == [-100, -200, -300, -400, -500]


def test_get_stock_prices() -> None:
    pass


def test_get_currency_rates() -> None:
    pass

