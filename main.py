import sys
import pandas as pd

from config import PATH_TO_EXCEL
from excel_reader import reader_excel
from services import transactions_with_phone_numbers
from utils import is_valid_date
from src.views import main_page
from src.reports import spending_by_workday


# sample_date = "2019-05-15 12:00:00"
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

main_page = main_page(user_date)
print("Вывести отчёт о транзакциями, содержащими в описании мобильные номера? Да/Нет\n")
while True:
    user_input1 = input().strip().lower()
    if "да" in user_input1:
        file = reader_excel(PATH_TO_EXCEL)
        r = transactions_with_phone_numbers(file)
        print(r)
        break
    elif "нет" in user_input1:
        break
    else:
        print("\nВведите да или нет")


print("Вывести отчёт о средних тратах за рабочие дни и выходные за три месяца? Да/Нет\n")
while True:
    user_input2 = input().strip().lower()
    if "да" in user_input2:
        transactions_ = pd.read_excel(PATH_TO_EXCEL)
        spending_by_workday(transactions_, user_date)
        sys.exit()
    elif "нет" in user_input2:
        print("\nДо свидания!")
        sys.exit()
    else:
        print("\nВведите да или нет")
