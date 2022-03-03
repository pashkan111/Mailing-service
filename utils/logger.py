import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Настраивает и возвращает экземпляр логгера
    """
    logger = logging.getLogger(name=name)

    if logger.hasHandlers() is False:
        formatter = logging.Formatter("[%(asctime)s %(levelname)s %(message)s")

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    return logger