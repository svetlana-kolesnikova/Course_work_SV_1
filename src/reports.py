# Траты в рабочий/выходной день
import functools
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import PATH_TO_DATA, PATH_TO_EXCEL
from main import filename, sample_date

transactions_ = pd.read_excel(PATH_TO_EXCEL)


def save_report(filename: str = None):
    """
    Декоратор для записи отчёта в файл.
    Если имя файла не передано, декоратор создаст файл с
    именем в формате 'report_{имя функции}_{текущая дата(YYYYMMDD_HHMMSS)}
    """

    def decorator(func):
        @functools.wraps(func)  # декоратор для сохранения метаинформации оригинальной функции
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Имя файла по умолчанию, если не передано
            output_file = filename or f'report_{func.__name__}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(PATH_TO_DATA / output_file, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"[INFO] Отчёт сохранён в файл: {output_file}")
            return result

        return wrapper

    return decorator


@save_report(filename if filename.strip() else None)
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)
    Если дата не передана, то берется текущая дата
    """
    # преобразование полученных данных столбца в dataframe
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    # проверяем задана ли дата
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(sample_date, "%Y-%m-%d %H:%M:%S")

    three_months_ago = end_date - relativedelta(months=3)  # получаем дату три месяца назад

    # получаем транзакции с начала месяца
    filter_operations = transactions[
        (transactions["Дата операции"] >= three_months_ago) & (transactions["Дата операции"] <= end_date)
    ].copy()

    # Добавляем колонку с днём недели: 0 — понедельник, 6 — воскресенье
    filter_operations["День недели"] = filter_operations["Дата операции"].dt.weekday

    # Определяем рабочий/выходной день
    filter_operations["Тип дня"] = filter_operations["День недели"].apply(lambda x: "Рабочий" if x < 5 else "Выходной")

    weekend_transactions = filter_operations[
        (filter_operations["Тип дня"] == "Выходной") & (filter_operations["Сумма операции"] < 0)
    ]

    average_weekend_transact = round(abs(weekend_transactions["Сумма операции"].mean()), 2)

    workday_transactions = filter_operations[
        (filter_operations["Тип дня"] == "Рабочий") & (filter_operations["Сумма операции"] < 0)
    ]

    average_workday_transact = round(abs(workday_transactions["Сумма операции"].mean()), 2)
    return (
        f"Средние траты в выходной день - {average_weekend_transact} руб.\n"
        f"Средние траты в рабочий день - {average_workday_transact} руб.\n"
    )


if __name__ == "__main__":
    print(transactions_.head())
    print(sample_date)
    print(spending_by_workday(transactions_, sample_date))
