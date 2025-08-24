import logging

def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logger.propagate = False

    return logger
