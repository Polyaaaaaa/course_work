from unittest.mock import MagicMock

from pandas import DataFrame

from src.reports import spending_by_weekday, get_weekday


# хорошо сделан, не нужно переделывать
def test_spending_by_weekday() -> None:
    data = DataFrame(
        [
            {
                "Дата операции": "31.12.2021 00:12:53",
                "Дата платежа": "31.12.2021",
                "Номер карты": "",
                "Статус": "OK",
                "Сумма операции": -800.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -800.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Переводы",
                "MCC": "",
                "Описание": "Константин Л.",
                "Бонусы (включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 800.0,
            },
            {
                "Дата операции": "30.12.2021 22:22:03",
                "Дата платежа": "31.12.2021",
                "Номер карты": "",
                "Статус": "OK",
                "Сумма операции": -20000.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -20000.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Переводы",
                "MCC": "",
                "Описание": "Константин Л.",
                "Бонусы (включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 20000.0,
            },
        ]
    )

    assert spending_by_weekday(data, "31.12.2021 10:20:23").to_dict(orient="records") == [
        {"День недели": "Понедельник", "Средние траты": 0.0},
        {"День недели": "Вторник", "Средние траты": 0.0},
        {"День недели": "Среда", "Средние траты": 0.0},
        {"День недели": "Четверг", "Средние траты": 20000.0},
        {"День недели": "Пятница", "Средние траты": 800.0},
        {"День недели": "Суббота", "Средние траты": 0.0},
        {"День недели": "Воскресенье", "Средние траты": 0.0},
    ]


# хорошо сделан скорее всего, не переделывать
def test_get_weekday() -> None:
    assert get_weekday("31.12.2021 00:12:53") == 5
