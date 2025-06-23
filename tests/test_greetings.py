from typing import Any

from src.greetings import greeting


def test_greeting_morning() -> Any:
    """
    Тестирование функции с периодом времени 06:00 - 11:59:59
    """
    assert greeting("2025-01-01 06:00:00") == "Доброе утро\n"
    assert greeting("2025-01-01 11:59:59") == "Доброе утро\n"


def test_greeting_day() -> Any:
    """
    Тестирование функции с периодом времени 12:00 - 17:59:59
    """
    assert greeting("2025-01-01 12:00:00") == "Добрый день\n"
    assert greeting("2025-01-01 17:59:00") == "Добрый день\n"


def test_greeting_evening() -> Any:
    """
    Тестирование функции с периодом времени 18:00 - 23:59:59
    """
    assert greeting("2025-01-01 18:00:00") == "Добрый вечер\n"
    assert greeting("2025-01-01 23:59:59") == "Добрый вечер\n"


def test_greeting_night() -> Any:
    """
    Тестирование функции с периодом времени 00:00 - 05:59:59
    """
    assert greeting("2025-01-01 00:00:00") == "Доброй ночи\n"
    assert greeting("2025-01-01 05:59:59") == "Доброй ночи\n"
