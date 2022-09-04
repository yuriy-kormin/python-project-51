import logging
import sys
LOGNAME = 'page_loader.log'


def setup_logger():
    logging.basicConfig(filename=LOGNAME, filemode='a',
                        encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s | %(levelname)s | %(message)s')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stdout_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(stdout_handler)
    logging.getLogger('').addHandler(stderr_handler)
