import os
import requests
from pageloader.parser import parse_html
from pageloader.content_actions import render_name
from pageloader.logger import get_logger

log = get_logger(__name__)
PATH = os.getcwd()


def download(url, running_path=None):
    global PATH, log
    if running_path:
        PATH = running_path
    log.info(f'requested url: {url}')
    request = requests.get(url)
    file_path = os.path.join(PATH, render_name(url, 'html'))
    log.info(f'output path:  {PATH}')
    log.info(f'write html file:  {file_path}')
    save_to_file(request.text, file_path)
    parse_html(url, file_path)
    return file_path


def save_to_file(data, path):
    try:
        log.debug(f'trying to save file by path: {path}')
        with open(path, 'w') as f:
            f.write(data)
    except Exception as e:
        log.warning(f'cannot write file, error:\n{e}')
        raise SystemExit()
