import os
import requests
import logging
from urllib.parse import urlparse
from progress.bar import Bar
import re


def download_files(url, work_dir, links_to_download):
    logging.debug('------ downloading content ------')
    if links_to_download:
        make_subdir(url, work_dir)
    errors = []
    with Bar('Downloading', max=len(links_to_download),
             suffix='%(percent)d%%') as bar:
        for url, path in links_to_download:
            bar.next()
            logging.debug(f'process url: {url}')
            try:
                request = make_request(url)
            except Exception as e:
                save_to_file(b'', path)
                errors.append(e)
                logging.debug(f'error raised\n{e}')
            else:
                save_to_file(request.content, path)
    return errors


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


def formatter(data):
    return re.sub(r'[^\da-zA-Z]', '-', data)


def render_name(url, output_type):
    url_parsed = urlparse(url)
    loc = formatter(url_parsed.netloc)
    path, ext = os.path.splitext(url_parsed.path)
    formatted_path = formatter(path)
    if output_type == 'html':
        return f"{loc}{formatted_path}.html"
    elif output_type == 'subdir':
        return f"{loc}{formatted_path}_files"
    elif output_type == 'file':
        if not ext:
            ext = '.html'
        return f"{loc}{formatted_path}{ext}"


def make_request(url):
    logging.debug('making request...')
    request = requests.get(url, stream=True)
    if request.status_code != 200:
        logging.exception(f'cannot fetch {url}')  # , exc_info=True)
        raise requests.exceptions.ConnectionError
    return request


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
