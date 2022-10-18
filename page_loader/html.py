import logging
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from page_loader.naming import render_subdir_name, render_filename

attribute_mapping = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}


def process_html(page_data: str, url: str, output_dir: str) -> tuple:
    soup = BeautifulSoup(page_data, 'html.parser')
    downloads = []
    subdir_name = render_subdir_name(url)
    subdir_path = os.path.join(output_dir, subdir_name)
    logging.debug('------ analyzing page data ------')
    tags = [*soup('script'), *soup('link'), *soup('img')]
    for tag in tags:
        attr_name = attribute_mapping[tag.name]
        obj_link = tag.get(attr_name)
        if not need_download(url, obj_link):
            continue
        logging.debug(f' + {obj_link}({tag.name})')
        obj_link = get_valid_link(url, obj_link)
        file_name = render_filename(obj_link)
        download_path = os.path.join(subdir_path, file_name)
        relative_path = os.path.join(subdir_name, file_name)
        downloads.append((obj_link, download_path))
        tag[attr_name] = relative_path
    if not len(tags):
        logging.debug(' - nothing to process -')
    return soup.prettify(), downloads


def need_download(url: str, link: str) -> bool:
    if not link:
        return False
    root_url, obj_url = map(urlparse, (url, link))
    if (
        not obj_url.netloc
        or obj_url.netloc == root_url.netloc
    ):
        return True


def get_valid_link(url: str, link: str) -> str:
    if not urlparse(link).netloc:
        return urljoin(url, link)
    return link
