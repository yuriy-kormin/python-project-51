import logging
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from page_loader.naming import render_name


def process_html(page_data: str, url: str, output_dir: str) -> tuple:
    soup = BeautifulSoup(page_data, 'html.parser')
    downloads = []
    subdir_name = render_name(url, 'subdir')
    subdir_path = os.path.join(output_dir, subdir_name)
    logging.debug('------ analyzing page data ------')
    for obj in ('img', 'link', 'script'):
        logging.debug(f'* process <{obj}> tag *')
        tags = soup.findAll(obj)
        for tag in tags:
            obj_link = tag.get('src', tag.get('href'))
            if need_download(url, obj_link):
                logging.debug(f' + {obj_link}')
                obj_link = get_valid_link(url, obj_link)
                file_name = render_name(obj_link, 'file')
                download_path = os.path.join(subdir_path, file_name)
                relative_path = os.path.join(subdir_name, file_name)
                downloads.append((obj_link, download_path))
                if 'src' in tag.attrs:
                    tag['src'] = relative_path
                else:
                    tag['href'] = relative_path
            else:
                logging.debug(f' - {obj_link}')
        if not len(tags):
            logging.debug(' - nothing to process -')
    return soup.prettify(), downloads


def need_download(url: str, link: str) -> bool:
    if link:
        root_url, obj_url = map(urlparse, (url, link))
        if not obj_url.netloc or \
                obj_url.netloc == root_url.netloc:
            return True


def get_valid_link(url: str, link: str) -> str:
    if not urlparse(link).netloc:
        return urljoin(url, link)
    return link
