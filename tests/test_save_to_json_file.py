from typing import Any
from unittest.mock import mock_open, patch

from src.save_to_json_file import save_to_json_file


def test_save_success() -> Any:
    """
    Тест для проверки открытия корректного файла и записи данных в него
    """
    data = [{"name": "test"}]
    file_path = "test.json"

    m = mock_open()
    with patch("builtins.open", m), patch("json.dump") as mock_json_dump:
        save_to_json_file(data, file_path)
        m.assert_called_once_with(file_path, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(data, m(), indent=4, ensure_ascii=False)


def test_save_failure_logs_error() -> Any:
    """
    Тест для проверки записи об ошибке при открытии некорректного файла
    """
    data = [{"name": "test"}]
    file_path = "invalid_path/test.json"

    with (
        patch("builtins.open", side_effect=IOError("File error")),
        patch("src.save_to_json_file.logger.error") as mock_logger_error,
    ):
        save_to_json_file(data, file_path)
        mock_logger_error.assert_called()
        assert "Произошла ошибка" in mock_logger_error.call_args[0][0]
