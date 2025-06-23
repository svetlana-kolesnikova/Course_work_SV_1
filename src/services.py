import re

from config import PATH_TO_DATA, PATH_TO_EXCEL
from src.excel_reader import reader_excel
from src.save_to_json_file import save_to_json_file

file = reader_excel(PATH_TO_EXCEL)

pattern = re.compile(r"7 \d{3} \d{3}-\d{2}-\d{2}")


def transactions_with_phone_numbers(transactions_list: list) -> list:
    """Функция отфильтровывает транзакции с телефонными номерами"""
    filtered = []
    for transaction in transactions_list:
        description = str(transaction.get("Описание", "")).strip()
        if pattern.search(description):
            filtered.append(transaction)
    return filtered


if __name__ == "__main__":

    print(transactions_with_phone_numbers(file))
    filtered_ = transactions_with_phone_numbers(file)

    output_file = PATH_TO_DATA / "filtered_result.json"

    save_to_json_file(filtered_, output_file)
