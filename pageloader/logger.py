import logging
LOGNAME = 'page_loader.log'


def set_log_path(path):
    logging.basicConfig(filename=LOGNAME, filemode='a',
                        encoding='utf-8', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
