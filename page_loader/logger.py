import logging
import sys


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_formatter = logging.Formatter(
        '%(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    stdout_handler.addFilter(
        lambda par: 0 if par.levelno != logging.INFO else 1)
    logger.addHandler(stdout_handler)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_formatter = logging.Formatter(
        '%(levelname)s | %(name)s | %(message)s')
    stderr_handler.setFormatter(stderr_formatter)
