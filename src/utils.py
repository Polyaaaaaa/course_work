from datetime import datetime, time
import logging

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def hi_message(date: str) -> str | None:
    """Функция, возращающая приветствие в зависимости от времени"""

    logger.info("Анализируем, какое приветствие выбрать")
    current_date = datetime.strptime(date, "%d:%m:%Y %H:%M:%S").time()

    hi_time = {"Доброй ночи!": time(23, 0, 0),
               "Доброе утро!": time(5, 0, 0),
               "Добрый день!": time(12, 0, 0),
               "Добрый вечер!": time(17, 0, 0)}

    for key, value in hi_time.items():
        if current_date <= value:
            logger.info(f"Приветствие будет: {key}")

    return None
