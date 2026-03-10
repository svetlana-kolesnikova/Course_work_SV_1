import json
import logging
import re

from config import PATH_TO_DATA, PATH_TO_EXCEL, PATH_TO_LOGS
from src.excel_reader import reader_excel
from src.save_to_json_file import save_to_json_file

file = reader_excel(PATH_TO_EXCEL)


logger = logging.getLogger("save_reports_transactions_with_phone_numbers")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_LOGS / "save_reports_transactions_with_phone_numbers.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Защита от повторного добавления обработчиков
if not logger.hasHandlers():
    logger.addHandler(file_handler)
logger.propagate = False

pattern = re.compile(r"7 \d{3} \d{3}-\d{2}-\d{2}")


def transactions_with_phone_numbers(transactions_list: list) -> str:
    """Функция отфильтровывает транзакции с телефонными номерами"""
    filtered = []
    logger.info("Вызов функции %s", transactions_with_phone_numbers.__name__)
    for transaction in transactions_list:
        description = str(transaction.get("Описание", "")).strip()
        if pattern.search(description):
            filtered.append(transaction)
    filtered_json = json.dumps(filtered, ensure_ascii=False, indent=4)
    logger.info("Функция завершила работу.")
    output_file = PATH_TO_DATA / "filtered_result.json"
    save_to_json_file(filtered, output_file)
    return filtered_json


# if __name__ == "__main__":
#
#     print(transactions_with_phone_numbers(file))
#     filtered_ = transactions_with_phone_numbers(file)
