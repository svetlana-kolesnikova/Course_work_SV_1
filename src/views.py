import json
from datetime import datetime

from config import PATH_TO_DATA
from save_to_json_file import save_to_json_file
from utils import (
    cards,
    currency_rates,
    get_operations_with_range,
    greeting,
    stock_prices,
    top_transactions,
)

file_ = PATH_TO_DATA / "main_page.json"


def main_page(date) -> str:
    """
    Функция для страницы "Главная"
    """
    main_json_response = {}
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    greeting_ = greeting(current_date)
    main_json_response["greeting"] = greeting_
    main_json_response["cards"] = cards(get_operations_with_range(date))
    main_json_response["top_transactions"] = top_transactions(get_operations_with_range(date))
    main_json_response["currency_rates"] = currency_rates()
    main_json_response["stock_prices"] = stock_prices()

    # Записываем данные в файл
    save_to_json_file(main_json_response, file_)

    json_response = json.dumps(main_json_response, ensure_ascii=False, indent=4)
    print(json_response)

    return json_response
