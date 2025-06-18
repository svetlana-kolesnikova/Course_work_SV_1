from typing import Any

from src.greetings import greeting, is_valid_date

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
