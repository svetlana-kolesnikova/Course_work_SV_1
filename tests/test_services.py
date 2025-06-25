import json

import pytest

from src.services import transactions_with_phone_numbers


@pytest.mark.parametrize(
    "input_data,expected_count",
    [
        (
            [
                {"Описание": "Тинькофф Мобайл +7 999 123-45-67"},
                {"Описание": "Перевод клиенту"},
                {"Описание": "Оплата по счёту"},
            ],
            1,
        ),
        (
            [
                {"Описание": "МТС +7 981 111-22-33"},
                {"Описание": "МегаФон 7 922 111-11-11"},
                {"Описание": "Яндекс Go"},
            ],
            2,
        ),
        (
            [
                {"Описание": "7 903 333-44-55"},  # формат без знака "+"
                {"Описание": "7 999 000-00-00"},
            ],
            2,
        ),
        (
            [
                {"Описание": "Нет номера тут"},
                {"Описание": ""},
                {"Описание": None},
            ],
            0,
        ),
    ],
)
def test_transactions_with_phone_numbers(input_data, expected_count):
    result = transactions_with_phone_numbers(input_data)
    # Преобразуем JSON-строку обратно в список
    result_list = json.loads(result)
    
    assert isinstance(result_list, list)
    assert len(result_list) == expected_count
