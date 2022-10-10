import logging

def get_logger(name: str = None):
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    file_handler_info = logging.FileHandler(filename="log_info.log")
    console.setLevel(logging.INFO)
    file_handler_info.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler_info)

    return logger