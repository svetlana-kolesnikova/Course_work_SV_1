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
    }
    df = pd.DataFrame(data)
    return df

# Заглушаем input и open
@patch("builtins.input", return_value="test_report.json")
@patch("builtins.open", new_callable=mock_open)
def test_spending_by_workday(mock_file, mock_input, sample_transactions):
    date = "2025-06-16 00:00:00"  # день после всех операций
    result = spending_by_workday(sample_transactions, date)

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
    
    assert written_content == expected_content
    
    