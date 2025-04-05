import logging
import os

LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "logging.log"
)


def setup_logger():
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(LOG_FILE_PATH)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_message(error):
    logger = setup_logger()
    logger.info(error)
