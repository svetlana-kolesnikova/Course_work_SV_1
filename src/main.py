from datetime import datetime
from greetings import greeting, is_valid_date
from excel_reader import reader_excel
from config import PATH_TO_EXCEL

print("Введите дату в формате 'YYYY-MM-DD HH:MM:SS':\n")

while True:
    user_input = input()
   
    if is_valid_date(user_input):
        current_date = user_input
        break
    else:
        print("Неверный формат даты. Попробуйте снова.\n")

print(greeting(current_date))
# print(greeting(current_date))
# excel_f = reader_excel(PATH_TO_EXCEL)
# print(excel_f)