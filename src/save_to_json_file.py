import json
import logging
from pathlib import Path
from typing import Union

from config import PATH_TO_LOGS

logger = logging.getLogger("save_to_json_file")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_LOGS / "save_to_json_file.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def save_to_json_file(data: list, file_path: Union[str, Path]) -> None:
    """
    Сохранение файла по указанному пути
    """
    try:
        logger.info(f"Записываем данные в файл {file_path}")
        with open(file_path, "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, indent=4, ensure_ascii=False)
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
