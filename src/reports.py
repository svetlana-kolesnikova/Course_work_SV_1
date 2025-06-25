# Траты в рабочий/выходной день
import functools
import json
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import PATH_TO_DATA, PATH_TO_EXCEL, PATH_TO_LOGS

transactions_ = pd.read_excel(PATH_TO_EXCEL)

logger = logging.getLogger("save_reports_spending_by_workday")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_LOGS / "save_reports_spending_by_workday.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def save_report():
    """
    Декоратор для записи отчёта в файл.
    Если имя файла не передано, декоратор создаст файл с
    именем в формате 'report_{имя функции}_{текущая дата(YYYYMMDD_HHMMSS)}
    """

    def decorator(func):
        @functools.wraps(func)  # декоратор для сохранения метаинформации оригинальной функции
        def wrapper(*args, **kwargs):
            logger.info("Вызов функции %s", func.__name__)
            result = func(*args, **kwargs)
            filename = input(
                'Введите имя файла в формате "имя.json"\n'
                "(оставьте пустым — имя будет сгенерировано автоматически):\n"
            ).strip()
            if not filename:

                # Имя файла по умолчанию, если не передано
                filename = f'report_{func.__name__}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            file_path = PATH_TO_DATA / filename

            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    if filename.lower().endswith(".json"):
                        json.dump(result, file, indent=4, ensure_ascii=False)
                        logger.info("Отчёт сохранён в JSON-файл: %s", filename)
                    else:
                        file.write(str(result))
                        logger.info("Отчёт сохранён в текстовый файл: %s", filename)
            except Exception as e:
                logger.error("Ошибка при сохранении файла %s: %s", filename, e)
                # print(f"[ERROR] Не удалось сохранить файл: {e}")
            return result

        return wrapper

    return decorator


@save_report()
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
        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

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
        (filter_operations["Тип дня"] == "Выходной")
        & (filter_operations["Сумма операции"] < 0)
        & (filter_operations["Статус"] == "OK")
    ]

    average_weekend_transact = round(abs(weekend_transactions["Сумма операции"].mean()), 2)

    workday_transactions = filter_operations[
        (filter_operations["Тип дня"] == "Рабочий")
        & (filter_operations["Сумма операции"] < 0)
        & (filter_operations["Статус"] == "OK")
    ]

    average_workday_transact = round(abs(workday_transactions["Сумма операции"].mean()), 2)
    print(
        {
            "Средние траты в выходной день": f"{average_weekend_transact} руб.",
            "Средние траты в рабочий день": f"{average_workday_transact} руб.",
        }
    )
    return {
        "Средние траты в выходной день": f"{average_weekend_transact} руб.",
        "Средние траты в рабочий день": f"{average_workday_transact} руб.",
    }


# if __name__ == "__main__":
#     print(transactions_.head())
#     print(sample_date)
#     print(spending_by_workday(transactions_, sample_date))
