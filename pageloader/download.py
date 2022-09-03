import os
import requests
from pageloader.parser import parse_page
from pageloader.content_actions import render_name
from pageloader.logger import set_log_path
import logging


def download(url, workdir_path=None):
    work_dir = workdir_path if workdir_path else os.getcwd()
    set_log_path(work_dir)
    logging.info(f'requested url: {url}')
    request = requests.get(url)
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    logging.info(f'output path:  {work_dir}')
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
