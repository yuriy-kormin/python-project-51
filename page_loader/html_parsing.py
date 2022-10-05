import logging
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from page_loader.render_names import render_name


def process_html(page_data: str, url: str, work_dir: str) -> tuple:
    soup = BeautifulSoup(page_data, 'html.parser')
    downloads = []
    subdir_name = render_name(url, 'subdir')
    subdir_path = os.path.join(work_dir, subdir_name)
    logging.debug('------ analyzing page data ------')
    for obj in ('img', 'link', 'script'):
        logging.debug(f'* process <{obj}> tag *')
        tags = soup.findAll(obj)
        for tag in tags:
            key = 'href' if tag.get('href') else 'src'
            obj_url = need_download(url, tag[key])
            if obj_url:
                logging.debug(f' + {tag}')
                file_name = render_name(obj_url, 'file')
                download_path = os.path.join(subdir_path, file_name)
                relative_path = os.path.join(subdir_name, file_name)
                downloads.append((obj_url, download_path))
                tag[key] = relative_path
            else:
                logging.debug(f' - {tag[key]}')
        if not len(tags):
            logging.debug(' - nothing to process -')
    return soup.prettify(), downloads


def need_download(url: str, obj_href: str) -> str:
    """ Check that address and  href on the same domain name and
    must be downloaded. return full link to download file or None
    if file will not be downloaded"""
    source_url, obj_url = map(urlparse, (url, obj_href))
    if not obj_url.netloc:
        return urljoin(url, obj_href)
    elif obj_url.netloc == source_url.netloc:
        return obj_href
    return
