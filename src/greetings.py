from datetime import datetime, time


def greeting(current_time: str) -> str:
    """
    Функция приветствия. Возвращает сообщение в зависимости от времени суток.
    """
    current_time_ = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").time()
    if time(6, 0) <= current_time_ <= time(11, 59, 59):
        return "Доброе утро\n"
    elif time(12, 0) <= current_time_ <= time(17, 59, 59):
        return "Добрый день\n"
    elif time(18, 0) <= current_time_ <= time(23, 59, 59):
        return "Добрый вечер\n"
    else:
        return "Доброй ночи\n"
