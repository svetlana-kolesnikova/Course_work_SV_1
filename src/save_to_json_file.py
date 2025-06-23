import json
import logging
from pathlib import Path
from typing import Union

from config import PATH_TO_DATA, PATH_TO_LOGS

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


if __name__ == "__main__":
    data = [
        {
            "title": "Jalisco usar\u00e1 Cybertrucks de Tesla para que sean patrullas como parte de su plan de seguridad para el Mundial 2026 en M\u00e9xico",
            "author": "Adolfo Res\u00e9ndiz",
            "description": "Jalisco se convirti\u00f3 en el primer estado de M\u00e9xico en incorporar el pol\u00e9mico y futurista Tesla Cybertruck como patrulla. La noticia fue confirmada por el gobernador Pablo Lemus durante el anuncio de una flotilla de 678 nuevos veh\u00edculos para la polic\u00eda estatal\u2026",
            "url": "https://www.xataka.com.mx/automovil/jalisco-usara-cybertrucks-tesla-sean-patrullas-como-parte-su-plan-seguridad-para-mundial-2026-mexico",
        },
        {
            "title": "Elon Musk transformou uma f\u00e1brica abandonada nos EUA no supercomputador mais poderoso do mundo; ningu\u00e9m pensou nos vizinhos",
            "author": "Xataka",
            "description": "Se n\u00e3o for controlada, a hist\u00f3ria do Colossus ser\u00e1 menos sobre o avan\u00e7o da intelig\u00eancia artificial e mais sobre o retrocesso do direito ao ar limpo.",
            "url": "https://www.terra.com.br/byte/elon-musk-transformou-uma-fabrica-abandonada-nos-eua-no-supercomputador-mais-poderoso-do-mundo-ninguem-pensou-nos-vizinhos,caab3e8ecfb1f92b551d379337e7f7142n8wbxau.html",
        },
        {
            "title": "What is a Corporate Bitcoin Treasury? The Strategy Behind Companies Holding Crypto",
            "author": "Jason Nelson",
            "description": "A growing number of companies are using Bitcoin to diversify their holdings and signal forward-thinking financial strategies.",
            "url": "https://decrypt.co/resources/what-is-a-corporate-bitcoin-treasury-the-strategy-behind-companies-holding-crypto",
        },
        {
            "title": "An American Problem",
            "author": "Reihan Salam, Jesse Arm",
            "description": "We cannot afford to excuse, indulge, or minimize political violence.",
            "url": "https://www.theatlantic.com/ideas/archive/2025/05/anti-semitism-violence/682943/",
        },
    ]
    file_ = PATH_TO_DATA / "save_to_json_file.json"
    save_to_json_file(data, file_)
