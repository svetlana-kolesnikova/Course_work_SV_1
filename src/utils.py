import json
import os
import re
from datetime import datetime, time
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from config import PATH_TO_EXCEL, PATH_TO_USER_SETTINGS
from services import pattern


def greeting(current_time: str) -> str:
    """
    Функция приветствия. Возвращает сообщение в зависимости от времени суток.
    """
    current_time_ = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").time()
    if time(6, 0) <= current_time_ <= time(11, 59, 59):
        return "Доброе утро"
    elif time(12, 0) <= current_time_ <= time(17, 59, 59):
        return "Добрый день"
    elif time(18, 0) <= current_time_ <= time(23, 59, 59):
        return "Добрый вечер"
    else:
        return "Доброй ночи"


pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


def is_valid_date(date_str: str) -> bool:
    """
    Функция для проверки валидности введённого формата даты пользователем
    """
    if not pattern.match(date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


def get_operations_with_range(date: str) -> pd.DataFrame:
    """
    Функция выдает транзакции за период от начала месяца до заданной пользователем даты
    """

    # Получаем первый день месяца
    date_start_str = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y.%m.01 00:00:00")

    # Получаем df из файла excel
    df = pd.read_excel(PATH_TO_EXCEL)

    # преобразование полученных данных столбца в dataframe
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    """Получаем транзакции с начала месяца"""
    filter_operations = df[
        (df["Дата операции"] >= date_start_str) & (df["Дата операции"] <= date) & (df["Статус"] == "OK")
    ].copy()
    return filter_operations


def cards(transactions: pd.DataFrame) -> list:
    """
    Функция выводит список карт с номерами, суммой трат и суммой кэшбека
    """

    # Удаляем строки, где ячейка "Номер карты" пустая
    transactions = transactions.dropna(subset=["Номер карты"])

    # Группируем по полному номеру карты
    grouped = (
        transactions.groupby("Номер карты")
        .agg(
            {
                # Фильтруем и складываем только отрицательные суммы (расходы)
                "Сумма операции": lambda x: round(abs(x[x < 0].sum()), 2),
                # Фильтруем и складываем кэшбек
                "Кэшбэк": lambda x: round(x.sum(), 2),
            }
        )
        .reset_index()
    )

    # Формируем список из словарей
    result = []
    for _, row in grouped.iterrows():
        result.append(
            {"card_number": row["Номер карты"], "total_spent": row["Сумма операции"], "cashback": row["Кэшбэк"]}
        )

    return result


def top_transactions(transactions: pd.DataFrame) -> list:
    """
    Функция выводит топ-5 транзакций по сумме платежа
    """
    # Сортировка по дате убыванию
    last_five = transactions.sort_values(by="Дата операции", ascending=False).head(5)

    # Формируем список из словарей
    result = []
    for _, row in last_five.iterrows():
        result.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": abs(row["Сумма операции"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return result


def load_user_settings() -> Any:
    """
    Функция для чтения файла user_settings.json
    """
    try:
        with open(PATH_TO_USER_SETTINGS, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Файл user_settings.json не найден.")
        return {"user_currencies": [], "user_stocks": []}


def currency_rates() -> list:
    """
    Функция выводит курсы валют из пользовательских настроек в файле user_settings.json
    """
    # Задаем адрес сайта, к которому хотим обратиться
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
    response = requests.get(url)

    # Получаем статус-код из ответа
    status_code = response.status_code

    # Проверяем, равен ли статус-код 200, то есть чтобы запрос был успешным
    if status_code == 200:

        # Преобразовываем ответ в формат json
        content = response.json()

        user_settings = load_user_settings()

        # Формируем список с полученными данными.
        currency_rates = [
            {"currency": code, "rate": content["Valute"][code]["Value"]}
            # Делаем отбор в полученном словаре по ключам валют из настроек пользователя
            for code in user_settings["user_currencies"]
            if code in content["Valute"]
        ]

        return currency_rates
    else:
        # Выводим сообщение об ошибке
        print(f"Запрос не был успешным. Возможная причина: {response.reason}")


load_dotenv()
API = os.getenv("API_KEY")


def stock_prices() -> list:
    """
    Функция запрашивает данные об акциях и выводит список в заданном формате
    """
    stock_prices_list = []
    user_settings = load_user_settings()

    # Перебор по значению ключа "user_stocks"
    for code in user_settings["user_stocks"]:

        # Задаем адрес сайта, к которому хотим обратиться
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={code}&apikey={API}"

        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.get(url)

        # Получаем статус-код из ответа
        status_code = response.status_code

        # Проверяем, равен ли статус-код 200, то есть чтобы запрос был успешным
        if status_code == 200:

            # Преобразовываем ответ в формат json
            stock_data = response.json()

            # Формируем список с полученными данными.
            try:
                quote = stock_data["Global Quote"]
                price = float(quote["02. open"])
                stock_prices_list.append({"stock": user_settings["user_stocks"], "price": round(price, 2)})

            # Отлавливаем ошибку при значении quote["02. open"] None
            except (KeyError, ValueError):
                stock_prices_list.append({"stock": user_settings["user_stocks"], "price": None})
        else:
            # Выводим сообщение об ошибке
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    return stock_prices_list
