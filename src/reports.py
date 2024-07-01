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
        operations: pd.DataFrame, date: str = None
) -> pd.DataFrame:
    sorted_by_date_list = []
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = [], [], [], [], [], [], []
    summ1, summ2, summ3, summ4, summ5, summ6, summ0 = 0, 0, 0, 0, 0, 0, 0

    weekdays = {}
    old_date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S') - relativedelta(months=-3)

    for element in operations:
        if element["Дата операции"]:
            if old_date <= datetime.strptime(str(element["Дата операции"]), '%d.%m.%Y %H:%M:%S') <= datetime.strptime(
                    str(date), '%d.%m.%Y %H:%M:%S'):

                sorted_by_date_list.append(element)

    for element in operations:
        if get_date(str(element["Дата операции"])) == 1:
            weekdays["Понедельник"] = 0
            monday.append(element["Сумма платежа"])
        elif get_date(str(element["Дата операции"])) == 2:
            weekdays["Вторник"] = 0
            tuesday.append(element["Сумма платежа"])
        elif get_date(str(element["Дата операции"])) == 3:
            weekdays["Среда"] = 0
            wednesday.append(element["Сумма платежа"])
        elif get_date(str(element["Дата операции"])) == 4:
            weekdays["Четверг"] = 0
            thursday.append(element["Сумма платежа"])
        elif get_date(str(element["Дата операции"])) == 5:
            weekdays["Пятница"] = 0
            friday.append(element["Сумма платежа"])
        elif get_date(str(element["Дата операции"])) == 6:
            weekdays["Суббота"] = 0
            saturday.append(element["Сумма платежа"])
        elif get_date(str(element["Дата операции"])) == 0:
            weekdays["Воскресенье"] = 0
            sunday.append(element["Сумма платежа"])
        else:
            continue

    for num in monday:
        summ1 += num
    for num in tuesday:
        summ2 += num
    for num in wednesday:
        summ3 += num
    for num in thursday:
        summ4 += num
    for num in friday:
        summ5 += num
    for num in saturday:
        summ6 += num
    for num in sunday:
        summ0 += num

    weekdays["Понедельник"] = summ1 / len(monday)
    weekdays["Вторник"] = summ2 / len(tuesday)
    weekdays["Среда"] = summ3 / len(wednesday)
    weekdays["Четверг"] = summ4 / len(thursday)
    weekdays["Пятница"] = summ5 / len(friday)
    weekdays["Суббота"] = summ6 / len(saturday)
    weekdays["Воскресенье"] = 0

    return pd.DataFrame(weekdays.items(), columns=['День недели', 'Средние траты'])


print(spending_by_weekday(get_operations_dict("C:\\Users\\Kir\\PycharmProjects\\pythonProject\\data\\operations.xls"),
                          "19.07.2019 20:27:51"))
#print(get_date("19.07.2019 20:27:51"))
