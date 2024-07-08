import unittest
from unittest.mock import patch
from datetime import datetime
from src.views import get_json_answer


def test_get_json_answer():
    with patch('requests.get') as mock_get:
        # Задаем ответ для первого запроса (валюты)
        mock_get.return_value.json.return_value = {
            "conversion_rates": {
                "USD": 75.31,
                "EUR": 89.24
            }
        }

        # Задаем ответ для второго запроса (акции)
        mock_get.return_value.json.return_value = [
            {"stock": "AAPL", "price": 133.15},
            {"stock": "AMZN", "price": 3345.23},
            {"stock": "GOOGL", "price": 2345.12},
            {"stock": "MSFT", "price": 255.14},
            {"stock": "TSLA", "price": 666.00}
        ]

        # Вызываем функцию get_json_answer с заданной датой
        result = get_json_answer("2022.01.01 12:00:00")

        # Проверяем, что функция вернула ожидаемый результат
        expected_result = {
            "greeting": "Добрый день",
            "cards": [
                {"last_digits": "1234", "total_spent": 12345.67, "cashback": 123.46},
                {"last_digits": "5678", "total_spent": 56789.10, "cashback": 567.89}
            ],
            "top_transactions": [
                {"date": "2021-12-31", "amount": -10000.00, "category": "Оплата услуг", "description": "Оплата телефона"},
                {"date": "2021-12-30", "amount": -5000.00, "category": "Покупки", "description": "Покупка в магазине"},
                {"date": "2021-12-29", "amount": -3000.00, "category": "Переводы", "description": "Перевод на карту"},
                {"date": "2021-12-28", "amount": -2000.00, "category": "Оплата услуг", "description": "Оплата коммунальных услуг"},
                {"date": "2021-12-27", "amount": -1000.00, "category": "Покупки", "description": "Покупка в интернете"}
            ],
            "currency_rates": [
                {"currency": "USD", "rate": 75.31},
                {"currency": "EUR", "rate": 89.24}
            ],
            "stock_prices": [
                {"stock": "AAPL", "price": 133.15},
                {"stock": "AMZN", "price": 3345.23},
                {"stock": "GOOGL", "price": 2345.12},
                {"stock": "MSFT", "price": 255.14},
                {"stock": "TSLA", "price": 666.00}
            ]
        }

        assert result == expected_result