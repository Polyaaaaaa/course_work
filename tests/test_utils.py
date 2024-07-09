from unittest.mock import patch

import pytest

from src.utils import get_card_num, hi_message


# хорошо сделан, не нужно переделывать
def test_get_card_num() -> None:
    assert get_card_num("*7197") == '"7197"'


# @pytest.mark.parametrize("time, greeting", ["2024.07.03 06:00:00, Доброе утро!"], ["2024.07.03 13:00:00, Добрый день!"], ["2024.07.03 18:00:00, Добрый вечер!"], ["2024.07.03 23:00:00, Доброй ночи!"])


# хорошо сделан, не нужно переделывать
def test_hi_message() -> None:
    assert hi_message("2024.07.03 06:00:00") == '"Доброе утро!"'
    assert hi_message("2024.07.03 13:00:00") == '"Добрый день!"'
    assert hi_message("2024.07.03 18:00:00") == '"Добрый вечер!"'
    assert hi_message("2024.07.03 23:00:00") == '"Доброй ночи!"'


# def test_get_top_of_transactions() -> None:
#     transactions = [
#         {"Сумма платежа": -100},
#         {"Сумма платежа": -200},
#         {"Сумма платежа": -300},
#         {"Сумма платежа": -400},
#         {"Сумма платежа": -500},
#         {"Сумма платежа": -600},
#         {"Сумма платежа": -700},
#     ]
#     result = get_top_of_transactions(transactions)
#     expected_result = [-500, -400, -300, -200, -100]
#     assert result == expected_result


# def test_get_stock_prices() -> None:
#     mock_response = {
#         "quoteResponse": {
#             "result": [
#                 {"symbol": "AAPL", "regularMarketPrice": 150.12},
#                 {"symbol": "AMZN", "regularMarketPrice": 3173.18},
#                 {"symbol": "GOOGL", "regularMarketPrice": 2742.39},
#                 {"symbol": "MSFT", "regularMarketPrice": 296.71},
#                 {"symbol": "TSLA", "regularMarketPrice": 1007.08},
#             ]
#         }
#     }
#     with patch("requests.get") as mock_get:
#         mock_get.return_value.json.return_value = mock_response
#         result = get_stock_prices()
#         mock_get.assert_called_once_with(
#             "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,AMZN,GOOGL,MSFT,TSLA"
#         )
#         assert result == "Ошибка"

#
# def test_get_currency_rates() -> None:
#     mock_response = {"rates": {"USD": 73.21, "EUR": 87.08}}
#     with patch("requests.get") as mock_get:
#         mock_get.return_value.json.return_value = mock_response
#         result = get_currency_rates()
#         mock_get.assert_called_once_with(
#             "https://api.apilayer.com/currency_data/live",
#             params={"base": "RUB", "symbols": "EUR,USD"},
#             headers={"apikey": "FZ3ahVSsZCDfaRFeuyZdRoIyOrzAzavs"},
#         )
#         assert result == "Ошибка"
