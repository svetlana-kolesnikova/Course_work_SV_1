import json
from datetime import datetime

from config import PATH_TO_DATA
from save_to_json_file import save_to_json_file
from utils import (
    cards,
    currency_rates,
    get_operations_with_range,
    greeting,
    is_valid_date,
    stock_prices,
    top_transactions,
)

file_ = PATH_TO_DATA / "main_page.json"


def main_page() -> str:
    """
    Функция для страницы "Главная"
    """
    main_json_response = {}
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    greeting_ = greeting(current_date)
    print(greeting_)
    print("Для фильтрации транзакций введите дату в формате 'YYYY-MM-DD HH:MM:SS':\n")

    while True:
        user_input = input()
        if is_valid_date(user_input):
            """
            Программа проверяет корректность введённого формата даты
            """
            user_date = user_input
            break
        else:
            print("Неверный формат даты. Попробуйте снова.\n")

    main_json_response["greeting"] = greeting_
    main_json_response["cards"] = cards(get_operations_with_range(user_date))
    main_json_response["top_transactions"] = top_transactions(get_operations_with_range(user_date))
    main_json_response["currency_rates"] = currency_rates()
    main_json_response["stock_prices"] = stock_prices()

    # Записываем данные в файл
    save_to_json_file(main_json_response, file_)

    json_response = json.dumps(main_json_response, ensure_ascii=False, indent=4)
    print(json_response)

    return json_response
