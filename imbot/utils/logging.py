import logging

def setup_logging():
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)
    return logger