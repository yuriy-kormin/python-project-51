import os
import requests
from pageloader.parser import parse_html, render_name
from pageloader.logger import logger


def download(address, path=None):
    if path is None:
        path = os.getcwd()
    log = logger(os.path.join(path, 'log'))
    log.debug(f'Try to download {address}')
    request = requests.get(address)
    file_path = os.path.join(path, render_name(address, 'html'))
    log.debug(f'saving to file  {file_path}')
    save_to_file(request.text, file_path)
    subdir_name = make_subdir(address, path)
    log.debug(f'making subdir   {subdir_name}')
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
