import os
import requests
from pageloader.parser import parse_html, render_name
from pageloader.logger import get_logger

log = None
PATH = os.getcwd()


def download(address, running_path=None):
    global PATH, log

    if running_path:
        PATH = running_path
    log = get_logger(__name__, os.path.join(PATH, 'log'))

    log.info(f'requested url: {address}')
    request = requests.get(address)
    file_path = os.path.join(PATH, render_name(address, 'html'))
    log.info(f'output path:  {PATH}')
    log.info(f'write html file:  {file_path}')
    save_to_file(request.text, file_path)
    subdir_name = make_subdir(address, PATH)
    parse_html(address, file_path, subdir_name)
    return file_path


def make_subdir(address, path):
    name = render_name(address, 'subdir')
    subdir_path = os.path.join(path, name)
    # try:
    os.makedirs(subdir_path, exist_ok=True)
    # except:

    return subdir_path


def save_to_file(data, path):
    with open(path, 'w') as f:
        f.write(data)
