import json
from typing import Any
from unittest.mock import patch, mock_open

import pandas as pd
import pytest

from src.utils import greeting, is_valid_date, get_operations_with_range, cards, top_transactions, load_user_settings, \
    stock_prices, currency_rates


def test_greeting_morning() -> Any:
    """
    Тестирование функции с периодом времени 06:00 - 11:59:59
    """
    assert greeting("2025-01-01 06:00:00") == "Доброе утро"
    assert greeting("2025-01-01 11:59:59") == "Доброе утро"


def test_greeting_day() -> Any:
    """
    Тестирование функции с периодом времени 12:00 - 17:59:59
    """
    assert greeting("2025-01-01 12:00:00") == "Добрый день"
    assert greeting("2025-01-01 17:59:00") == "Добрый день"


def test_greeting_evening() -> Any:
    """
    Тестирование функции с периодом времени 18:00 - 23:59:59
    """
    assert greeting("2025-01-01 18:00:00") == "Добрый вечер"
    assert greeting("2025-01-01 23:59:59") == "Добрый вечер"


def test_greeting_night() -> Any:
    """
    Тестирование функции с периодом времени 00:00 - 05:59:59
    """
    assert greeting("2025-01-01 00:00:00") == "Доброй ночи"
    assert greeting("2025-01-01 05:59:59") == "Доброй ночи"


@pytest.mark.parametrize("date_str,expected", [
    ("2025-06-25 13:00:00", True),
    ("2025-13-25 13:00:00", False),  # неверный месяц
    ("25-06-2025 13:00:00", False),  # неверный формат
    ("2025-06-25", False),           # нет времени
])


def test_is_valid_date(date_str, expected):
    assert is_valid_date(date_str) == expected


def test_valid_dates() -> Any:
    """
    Тестирование валидной даты
    """
    assert is_valid_date("2025-06-19 14:30:00")
    assert is_valid_date("1999-12-31 23:59:59")
    assert is_valid_date("2020-02-29 00:00:00")  # високосный год


def test_invalid_format() -> Any:
    """
    Тестирование с неверным форматом ввода
    """
    assert not is_valid_date("2025/06/19 14:30:00")  # неправильный разделитель
    assert not is_valid_date("19-06-2025 14:30:00")  # другой порядок
    assert not is_valid_date("2025-6-9 4:3:0")       # недостаточная длина


def test_invalid_values() -> Any:
    """
    Тестирование с несуществующими параметрами
    """
    assert not is_valid_date("2025-02-30 12:00:00")  # несуществующая дата
    assert not is_valid_date("2025-06-19 25:00:00")  # часы > 24
    assert not is_valid_date("2025-06-19 23:60:00")  # минуты > 59

def mock_transactions_df():
    return pd.DataFrame({
        "Дата операции": pd.to_datetime([
            "2025-06-01", "2025-06-15", "2025-06-25", "2025-05-30"
        ]),
        "Сумма операции": [-1000, -2000, -500, -300],
        "Кэшбэк": [10, 20, 5, 0],
        "Статус": ["OK", "OK", "FAILED", "OK"],
        "Номер карты": ["1234", "1234", "1234", None],
        "Категория": ["Еда", "Транспорт", "Еда", "Сервисы"],
        "Описание": ["Кафе", "Метро", "Пицца", "Подписка"]
    })


@patch("src.excel_reader.pd.read_excel")
def test_get_operations_with_range(mock_read_excel):
    mock_read_excel.return_value = mock_transactions_df()
    
    date = "2025-06-25 00:00:00"
    df = get_operations_with_range(date)
    
    assert not df.empty
    assert all(df["Статус"] == "OK")
    assert df["Дата операции"].min() >= pd.to_datetime("2025-06-01")
    assert df["Дата операции"].max() <= pd.to_datetime("2025-06-25")


def test_cards():
    df = mock_transactions_df()
    df = df[df["Статус"] == "OK"]
    result = cards(df)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["card_number"] == "1234"
    assert result[0]["total_spent"] == 3000  # -1000 + -2000
    assert result[0]["cashback"] == 30  # 10 + 20


def test_top_transactions():
    df = mock_transactions_df()
    result = top_transactions(df)
    
    assert isinstance(result, list)
    assert len(result) == 4  # Один элемент будет с "FAILED" статусом
    for item in result:
        assert "date" in item and "amount" in item and "category" in item and "description" in item
        

def test_load_user_settings_file_found():
    """
    Тест загрузки настроек, если файл найден
    """
    mock_data = json.dumps({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "MSFT"]})

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_user_settings()
        assert result == {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "MSFT"]}
        

def test_load_user_settings_file_not_found():
    """
    Тест загрузки настроек, если файл отсутствует
    """
    with patch("builtins.open", side_effect=FileNotFoundError()):
        result = load_user_settings()
        assert result == {"user_currencies": [], "user_stocks": []}
        

@patch("src.utils.load_user_settings")
@patch("src.utils.requests.get")
def test_currency_rates(mock_get, mock_settings):
    """
    Тест функции получения курсов валют
    """
    mock_settings.return_value = {"user_currencies": ["USD", "EUR"]}
    mock_response = {
        "Valute": {
            "USD": {"Value": 90.0},
            "EUR": {"Value": 100.0}
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = currency_rates()

    assert isinstance(result, list)
    assert result == [
        {"currency": "USD", "rate": 90.0},
        {"currency": "EUR", "rate": 100.0}
    ]


@patch("src.utils.load_user_settings")
@patch("src.utils.requests.get")
def test_stock_prices(mock_get, mock_settings):
    """
    Тест функции получения цен акций
    """
    mock_settings.return_value = {"user_stocks": ["AAPL"]}
    mock_response = {
        "Global Quote": {
            "02. open": "192.50"
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = stock_prices()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["stock"] == ["AAPL"]
    assert result[0]["price"] == 192.5


@patch("src.utils.load_user_settings")
@patch("src.utils.requests.get")
def test_stock_prices_with_invalid_response(mock_get, mock_settings):
    """
    Тест обработки некорректного JSON-ответа от API
    """
    mock_settings.return_value = {"user_stocks": ["AAPL"]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}  # пустой ответ

    result = stock_prices()

    assert isinstance(result, list)
    assert result[0]["stock"] == ["AAPL"]
    assert result[0]["price"] is None
