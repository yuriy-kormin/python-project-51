import logging
import os
from page_loader.naming import render_name


def check_dir(output):
    if not os.path.isdir(output):
        logging.error("Output directory doesn't exists")
        raise FileNotFoundError


def save_to_file(data, path, mode='wb'):
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


def make_subdir(url, work_dir):
    subdir_name = render_name(url, 'subdir')
    path = os.path.join(work_dir, subdir_name)
    try:
        logging.debug(f'trying to make subdir {path}')
        os.makedirs(path, exist_ok=True)
        logging.debug('subdir created successfully')
    except OSError:
        logging.exception('cannot make subdir', exc_info=True)
        raise
