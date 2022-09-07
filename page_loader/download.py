import os
from page_loader.analize_content import process_main_page
from page_loader.logger import setup_logger
import logging


def check_dir(output):
    if not os.path.isdir(output):
        logging.error("Output directory doesn't exists")
        raise FileNotFoundError
    elif not os.access(output, os.W_OK):
        logging.error("Write permissions error")
        raise PermissionError


def download(url, output=None):
    work_dir = output if output else os.getcwd()
    check_dir(work_dir)
    setup_logger()
    logging.info(f'requested url: {url}')
    logging.info(f'output path:  {work_dir}')
    return process_main_page(url, work_dir)
