import os
import sys

import requests
from pageloader.parser import parse_page
from pageloader.content_actions import render_name
from pageloader.logger import setup_logger
import logging


def download(url, output=None):
    work_dir = output if output else os.getcwd()
    setup_logger()
    logging.info(f'requested url: {url}')
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    logging.info(f'output path:  {work_dir}')
    if not os.path.exists(work_dir):
        logging.error('output path does not exists')
        sys.exit(0)
    request = requests.get(url)
    logging.info(f'write html file:  {file_path}')
    save_to_file(request.text, file_path)
    parse_page(url, file_path)
    return file_path


def save_to_file(data, path):
    try:
        logging.debug(f'trying to save file by path: {path}')
        with open(path, 'w') as f:
            f.write(data)
    except Exception:
        logging.exception('cannot write file', exc_info=True)
        raise SystemExit()
