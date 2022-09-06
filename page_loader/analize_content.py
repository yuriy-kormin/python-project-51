from urllib.parse import urljoin
import os
from bs4 import BeautifulSoup
from page_loader.content_actions import render_name, url_parse
import logging


def parse_page(file_path):
    workdir_name, _ = os.path.split(file_path)
    logging.debug(f'parsing html {file_path}')
    try:
        with open(file_path, 'r') as f:
            file_data = f.read()
        logging.debug('file successfully read, processing to BS4')
        soup = BeautifulSoup(file_data, 'html.parser')
        logging.debug('file successfully parsed by BS4')
    except (FileNotFoundError, PermissionError):
        logging.exception(f'Cannot parse file {file_path}',
                          exc_info=True)
        raise
    return soup


def process_soup(soup, url, work_dir):
    links_to_download = []
    subdir_name = render_name(url, 'subdir')
    subdir = os.path.join(work_dir, subdir_name)
    for obj in ('img', 'link', 'script'):
        key = 'src' if obj == 'img' else 'href'
        logging.debug(f'* process <{obj}> tag *')
        tags = soup.findAll(obj, {key: True})
        for tag in tags:
            logging.debug(f'processing {tag[key]}')
            obj_url = need_to_download(url, tag[key])
            if obj_url:
                logging.debug(f' + download {obj_url}')
                file_name = render_name(obj_url, 'file')
                local_path = os.path.join(subdir, file_name)
                links_to_download.append((obj_url, local_path))
                tag[key] = local_path
            else:
                logging.debug(' - passing')
        if not len(tags):
            logging.debug(' - nothing to process -')
    return links_to_download


def need_to_download(url: str, obj_href: str) -> str:
    """ Check that address and  href on the same domain name and
    must be downloaded. return full link to download file or None
    if file will not be downloaded"""
    source_url, obj_url = map(url_parse, (url, obj_href))
    if not obj_url['loc']:
        return urljoin(url, obj_href)
    _, ext = os.path.splitext(obj_url['full_path'])
    if obj_url['loc'] == source_url['loc']:
        return obj_href
    return
