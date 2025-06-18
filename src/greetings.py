from datetime import datetime, time

import re

pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

def is_valid_date(date_str: str) -> bool:
    if not pattern.match(date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


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
