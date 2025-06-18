from typing import Any
from unittest.mock import Mock, patch

from src.excel_reader import reader_excel


def test_reader_excel_success() -> Any:
    """Тест при успешном чтении файла excel"""
    fake_data = [{"id": 1, "state": "done", "amount": 100}, {"id": 2, "state": "pending", "amount": 200}]

    mock_df = Mock()
    mock_df.to_dict.return_value = fake_data

    with patch("pandas.read_excel", return_value=mock_df):
        result = reader_excel("fake_path.xlsx")
        assert result == fake_data
        mock_df.to_dict.assert_called_once_with(orient="records")


def test_reader_excel_file_not_found() -> Any:
    """Тест при отсутствии файла excel"""
    result = reader_excel("non_existent_file.xlsx")
    assert result == []