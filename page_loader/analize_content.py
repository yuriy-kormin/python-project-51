from urllib.parse import urljoin, urlparse
import os
from bs4 import BeautifulSoup
from page_loader.content_actions import render_name, \
    make_request, download_files, save_to_file, make_subdir
import logging


def process_main_page(url, work_dir):
    page_data = make_request(url).text
    processed_html, download_list = process_html(page_data, url, work_dir)
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    save_to_file(processed_html, file_path, mode='w')
    if download_list:
        make_subdir(url, work_dir)
    errors = download_files(download_list)
    if len(errors):
        error_str = "\n    ".join(errors)
        logging.info(
            f'Page was partially downloaded, some errors occur: \n{error_str}')
    else:
        logging.info(f"Page was successfully downloaded as '{file_path}'")
    return file_path


def process_html(page_data: str, url: str, work_dir: str) -> tuple:
    soup = BeautifulSoup(page_data, 'html.parser')
    links_to_download = process_soup(soup, url, work_dir)
    return soup.prettify(), links_to_download


def process_soup(soup, url, work_dir):
    links_to_download = []
    subdir_name = render_name(url, 'subdir')
    subdir_full_path = os.path.join(work_dir, subdir_name)
    logging.debug('------ analyzing page data ------')
    for obj in ('img', 'link', 'script'):
        logging.debug(f'* process <{obj}> tag *')
        tags = soup.findAll(obj)
        for tag in tags:
            key = 'href' if tag.get('href') else 'src'
            obj_url = need_to_download(url, tag[key])
            if obj_url:
                logging.debug(f' + {tag}')
                file_name = render_name(obj_url, 'file')
                local_path = os.path.join(subdir_full_path, file_name)
                relative_path = os.path.join(subdir_name, file_name)
                links_to_download.append((obj_url, local_path))
                tag[key] = relative_path
            else:
                logging.debug(f' - {tag[key]}')
        if not len(tags):
            logging.debug(' - nothing to process -')
    return links_to_download


def need_to_download(url: str, obj_href: str) -> str:
    """ Check that address and  href on the same domain name and
    must be downloaded. return full link to download file or None
    if file will not be downloaded"""
    source_url, obj_url = map(urlparse, (url, obj_href))
    if not obj_url.netloc:
        return urljoin(url, obj_href)
    elif obj_url.netloc == source_url.netloc:
        return obj_href
    return
