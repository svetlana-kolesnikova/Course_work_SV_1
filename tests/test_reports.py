from datetime import datetime

import pytest
import pandas as pd
from unittest.mock import patch, mock_open, call
import json

from src.reports import spending_by_workday  # ← замени на путь к твоему модулю


@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [
            "2025-06-15",  # выходной
            "2025-06-14",  # выходной
            "2025-06-13",  # рабочий
            "2025-06-12",  # рабочий
        ],
        "Сумма операции": [-1000.0, -500.0, -300.0, -700.0],
        "Статус": ["OK", "OK", "OK", "OK"]
    }
    df = pd.DataFrame(data)
    return df

# Заглушаем input и open
@patch("builtins.input", return_value="test_report.json")
@patch("builtins.open", new_callable=mock_open)
def test_spending_by_workday(mock_file, mock_input, sample_transactions):
    date = "2025-06-16 00:00:00"  # день после всех операций
    result = spending_by_workday(sample_transactions, "2025-06-16 00:00:00")

    # Проверим, что результат содержит ожидаемые строки
    assert isinstance(result, dict)
    assert "Средние траты в выходной день" in result
    assert "Средние траты в рабочий день" in result
    
    # Проверим, что файл открывался для записи
    mock_file.assert_called_once()
    handle = mock_file()
    
    # Проверим, что в файл записывалось то же, что и вернуло тело функции
    # Получим то, что писалось в файл
    written_content = ''.join(call.args[0] for call in handle.write.call_args_list)
    # Преобразуем результат функции в строку JSON (как должно было быть сохранено)
    expected_content = json.dumps(result, indent=4, ensure_ascii=False)
    assert json.loads(written_content) == result
    assert written_content == expected_content
    

@patch("builtins.input", return_value="bad_report.json")
@patch("builtins.open", side_effect=IOError("permission denied"))
@patch("src.reports.logger")  # замените путь к логгеру
def test_spending_by_workday_file_error(mock_logger, mock_open, mock_input, sample_transactions):
    """Обрабатываем исключение при сохранении файла"""
    result = spending_by_workday(sample_transactions, "2025-06-16 00:00:00")
    # Проверим, что в лог записана ошибка
    mock_logger.error.assert_called_once()
    assert "Ошибка при сохранении файла" in mock_logger.error.call_args[0][0]


@patch("builtins.input", return_value="report.json")
@patch("builtins.open", new_callable=mock_open)
def test_spending_by_workday_no_date(mock_file, mock_input, sample_transactions):
    """дата по умолчанию (None)"""
    result = spending_by_workday(sample_transactions)  # date=None по умолчанию
    assert isinstance(result, dict)
    handle = mock_file()
    written = ''.join(call.args[0] for call in handle.write.call_args_list)
    assert json.loads(written) == result


@patch("builtins.input", return_value="")  # пустой ввод
@patch("builtins.open", new_callable=mock_open)
@patch("src.reports.datetime")  # ← замени путь
def test_spending_by_workday_auto_filename(mock_datetime, mock_file, mock_input, sample_transactions):
    """имя не задано → генерируется автоматически"""
    mock_datetime.now.return_value = datetime(2025, 6, 25, 14, 0, 0)
    mock_datetime.strptime = datetime.strptime
    mock_datetime.strftime = datetime.strftime
    
    result = spending_by_workday(sample_transactions, "2025-06-25 15:00:00")
    
    # Проверяем что open был вызван с сгенерированным именем
    expected_filename_part = "report_spending_by_workday_20250625_140000.json"
    assert any(expected_filename_part in str(call_args[0][0]) for call_args in mock_file.call_args_list)
    

@patch("builtins.input", return_value="report.txt")
@patch("builtins.open", new_callable=mock_open)
def test_spending_by_workday_text_output(mock_file, mock_input, sample_transactions):
    result = spending_by_workday(sample_transactions, "2025-06-16 00:00:00")
    handle = mock_file()
    written = ''.join(call.args[0] for call in handle.write.call_args_list)
    # Проверка, что результат сериализован строкой
    assert isinstance(written, str)
    assert "Средние траты" in written
    