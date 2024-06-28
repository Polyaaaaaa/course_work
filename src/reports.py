from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import logging
from typing import Optional
from src.services import get_operations_dict

import pandas as pd


def get_date(date):
    date_obj = datetime.strptime(date, "%d.%m.%Y")
    weekday = date_obj.isocalendar()
    return weekday[2]


def spending_by_weekday(
    operations: pd.DataFrame, date: str = datetime.now()
) -> pd.DataFrame:
    sorted_by_date_list = []
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = [], [], [], [], [], [], []
    summ1, summ2, summ3, summ4, summ5, summ6, summ0 = 0, 0, 0, 0, 0, 0, 0

    weekdays = {}
    old_date = datetime.strptime(date, '%d.%m.%Y') - relativedelta(months=-3)
    for element in operations:
        print(element["Дата платежа"])
        if element["Дата платежа"] != "nan":
            if old_date <= datetime.strptime(str(element["Дата платежа"]), '%d.%m.%Y') <= datetime.strptime(str(date), '%d.%m.%Y'):
                sorted_by_date_list.append(element)
            print(element)
        elif element["Дата платежа"] == "nan":
            continue



    for element in operations:
        if get_date(element["Дата платежа"]) == 1:
            weekdays["Понедельник"] = 0
            monday.append(element["Сумма платежа"])
        elif get_date(element["Дата платежа"]) == 2:
            weekdays["Вторник"] = 0
            tuesday.append(element["Сумма платежа"])
        elif get_date(element["Дата платежа"]) == 3:
            weekdays["Среда"] = 0
            wednesday.append(element["Сумма платежа"])
        elif get_date(element["Дата платежа"]) == 4:
            weekdays["Четверг"] = 0
            thursday.append(element["Сумма платежа"])
        elif get_date(element["Дата платежа"]) == 5:
            weekdays["Пятница"] = 0
            friday.append(element["Сумма платежа"])
        elif get_date(element["Дата платежа"]) == 6:
            weekdays["Суббота"] = 0
            saturday.append(element["Сумма платежа"])
        elif get_date(element["Дата платежа"]) == 0:
            weekdays["Воскресенье"] = 0
            sunday.append(element["Сумма платежа"])

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
    weekdays["Воскресенье"] = summ0 / len(sunday)

    return pd.DataFrame(weekdays.items(), columns=['День недели', 'Средние траты'])


print(spending_by_weekday(get_operations_dict("C:\\Users\\Kir\\PycharmProjects\\pythonProject\\data\\operations.xls"),
                          "19.07.2019"))
#print(get_date("19.07.2019"))