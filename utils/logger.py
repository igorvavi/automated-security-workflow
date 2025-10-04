import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_path: str, verbose: bool = False) -> logging.Logger:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # file handler
    fh = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=2)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(ch)

    return logger
