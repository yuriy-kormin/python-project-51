import os
import requests
import logging
from urllib.parse import urlparse
from progress.bar import Bar
import re


def download_files(url, work_dir, links_to_download):
    logging.debug('------ process downloading ------')
    with Bar('Downloading', max=len(links_to_download),
             suffix='%(percent)d%%') as bar:
        if links_to_download:
            make_subdir(url, work_dir)
            logging.debug('------ downloading content ------')
            for url, path in links_to_download:
                bar.next()
                logging.debug(f'process url: {url}')
                request = make_request(url)
                save_to_file(request.content, path)


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


def replace_symbols(data):
    return re.sub(r'[^\da-zA-Z]', '-', data)


def render_name(url, output_type):
    url_data = url_parse(url)
    if output_type == 'html':
        return f"{url_data['loc']}{url_data['path']}.html"
    elif output_type == 'subdir':
        return f"{url_data['loc']}{url_data['path']}_files"
    elif output_type == 'file':
        name, ext = os.path.splitext(url_data['full_path'])
        name = replace_symbols(name)
        if not ext:
            ext = '.html'
        return f"{url_data['loc']}{name}{ext}"


def url_parse(url):
    url_parsed = urlparse(url)
    return {'netloc': url_parsed.netloc,
            'loc': replace_symbols(url_parsed.netloc),
            'path': replace_symbols(os.path.splitext(url_parsed.path)[0]),
            'full_path': url_parsed.path
            }


def make_request(url):
    try:
        request = requests.get(url, stream=True)
        request.raise_for_status()
        logging.debug('request complete')
    except Exception:
        logging.exception(f'cannot fetch {url}')
        raise requests.exceptions.HTTPError
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
    logging.debug(' ')
