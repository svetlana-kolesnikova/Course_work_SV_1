from datetime import datetime
import pandas as pd

from config import PATH_TO_EXCEL
from excel_reader import reader_excel
from greetings import greeting
from src.views import is_valid_date
from src.reports import spending_by_workday


sample_date = "2019-05-15 12:00:00"
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
        user_data = user_input
        # current_date = user_input
        break
    else:
        print("Неверный формат даты. Попробуйте снова.\n")

print("Вывести отчёт о средних тратах за рабочие дни и выходные? Да/Нет\n")
user_input1 = input().strip().lower()
if "да" in user_input1:
    transactions_ = pd.read_excel(PATH_TO_EXCEL)
    spending_by_workday(transactions_, user_data)
    
    
    



# print(greeting_))
# print(greeting(current_date))
# excel_f = reader_excel(PATH_TO_EXCEL)
# print(excel_f)
# print(current_datetime)
# print(user_data)
