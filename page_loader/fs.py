import logging
import os
from page_loader.naming import render_subdir_name


def check_dir(output_dir: str):
    if not os.path.isdir(output_dir):
        logging.error("Output directory doesn't exists")
        raise FileNotFoundError


def save_to_file(data: str, path: str, mode: str = 'wb'):
    _, ext = os.path.splitext(path)
    if mode != 'wb':
        logging.info(f'write html file:  {path}')
    try:
        logging.debug(f"trying to save file: '{path}'")
        with open(path, mode) as f:
            f.write(data)
    except OSError:
        logging.exception('cannot write file', exc_info=True)
        raise
    logging.debug('saving file successfully')


def make_subdir(url: str, output_dir: str):
    subdir_name = render_subdir_name(url)
    subdir_path = os.path.join(output_dir, subdir_name)
    try:
        logging.debug(f'trying to make subdir {subdir_path}')
        os.makedirs(subdir_path, exist_ok=True)
        logging.debug('subdir created successfully')
    except OSError:
        logging.exception('cannot make subdir', exc_info=True)
        raise
