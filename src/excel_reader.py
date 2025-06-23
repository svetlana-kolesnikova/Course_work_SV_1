from typing import Any, Dict, List, cast

import pandas as pd


def reader_excel(path: Any) -> List[Dict[Any, Any]]:
    """
    Функция для чтения файла excel. Возвращает список словарей с транзакциями
    """
    try:
        reader = pd.read_excel(path)
        financial_operations_excel = reader.to_dict(orient="records")
        return cast(List[Dict[Any, Any]], financial_operations_excel)
    except (FileNotFoundError, Exception):
        return []
