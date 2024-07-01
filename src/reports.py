from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import logging
from typing import Optional
from src.services import get_operations_dict

import pandas as pd


def get_date(date):
    date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    weekday = date_obj.isocalendar()
    return weekday[2]


def spending_by_weekday(
        operations: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
    operations = operations.to_dict(orient="records")
    sorted_by_date_list = []
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = [], [], [], [], [], [], []

    weekdays = {"Понедельник": 0, "Вторник": 0, "Среда": 0, "Четверг": 0, "Пятница": 0, "Суббота": 0, "Воскресенье": 0}
    old_date = date - relativedelta(months=3)

    for element in operations:
        if element["Дата операции"] and element["Сумма операции"] < 0:
            if old_date <= datetime.strptime((element["Дата операции"]), '%d.%m.%Y %H:%M:%S') <= date:

                sorted_by_date_list.append(element)

    for element in sorted_by_date_list:
        if get_date(str(element["Дата операции"])) == 1:
            monday.append(element["Сумма платежа"] * -1)
        elif get_date(str(element["Дата операции"])) == 2:
            tuesday.append(element["Сумма платежа"] * -1)
        elif get_date(str(element["Дата операции"])) == 3:
            wednesday.append(element["Сумма платежа"] * -1)
        elif get_date(str(element["Дата операции"])) == 4:
            thursday.append(element["Сумма платежа"] * -1)
        elif get_date(str(element["Дата операции"])) == 5:
            friday.append(element["Сумма платежа"] * -1)
        elif get_date(str(element["Дата операции"])) == 6:
            saturday.append(element["Сумма платежа"] * -1)
        elif get_date(str(element["Дата операции"])) == 7:
            sunday.append(element["Сумма платежа"] * -1)
        else:
            continue

    if len(monday) <= 0:
        weekdays["Понедельник"] = sum(monday) / 1
    else:
        weekdays["Понедельник"] = sum(monday) / len(monday)
    if len(tuesday) <= 0:
        weekdays["Вторник"] = sum(tuesday) / 1
    else:
        weekdays["Вторник"] = sum(tuesday) / len(tuesday)
    if len(wednesday) <= 0:
        weekdays["Среда"] = sum(wednesday) / 1
    else:
        weekdays["Среда"] = sum(wednesday) / len(wednesday)
    if len(thursday) <= 0:
        weekdays["Четверг"] = sum(thursday) / 1
    else:
        weekdays["Четверг"] = sum(thursday) / len(thursday)
    if len(friday) <= 0:
        weekdays["Пятница"] = sum(friday) / 1
    else:
        weekdays["Пятница"] = sum(friday) / len(friday)
    if len(saturday) <= 0:
        weekdays["Суббота"] = sum(saturday) / 1
    else:
        weekdays["Суббота"] = sum(saturday) / len(saturday)
    if len(sunday) <= 0:
        weekdays["Воскресенье"] = sum(sunday) / 1
    else:
        weekdays["Воскресенье"] = sum(sunday) / len(sunday)

    return pd.DataFrame(weekdays.items(), columns=['День недели', 'Средние траты'])


df = pd.read_excel('..\\data\\operations.xls')

print(spending_by_weekday(df, "20.06.2021 15:45:05"))
#print(get_date("30.06.2024 20:27:51"))
