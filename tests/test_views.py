import json
from typing import Any
from unittest.mock import patch, MagicMock
import pytest

from src.views import main_page


@patch("src.views.save_to_json_file")
@patch("src.views.stock_prices", return_value=[{"stock": ["AAPL"], "price": 192.5}])
@patch("src.views.currency_rates", return_value=[{"currency": "USD", "rate": 90.5}])
@patch("src.views.top_transactions", return_value=[{"date": "25.06.2025", "amount": 100, "category": "Еда", "description": "Кафе"}])
@patch("src.views.cards", return_value=[{"card_number": "1234", "total_spent": 1000, "cashback": 50}])
@patch("src.views.get_operations_with_range")
@patch("src.views.greeting", return_value="Добрый день")
def test_main_page(mock_greeting, mock_ops, mock_cards, mock_top, mock_currency, mock_stock, mock_save) -> Any:
    """
    Тестирование работы модуля views.py
    """
    mock_ops.return_value = MagicMock()  # можно более точно замокать DataFrame при необходимости

    result = main_page("2025-06-25 13:00:00")
    result_dict = json.loads(result)

    assert isinstance(result_dict, dict)
    assert result_dict["greeting"] == "Добрый день"
    assert "cards" in result_dict
    assert "top_transactions" in result_dict
    assert "currency_rates" in result_dict
    assert "stock_prices" in result_dict

    mock_save.assert_called_once()  # проверяем, что файл сохранялся