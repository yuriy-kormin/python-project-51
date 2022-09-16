from urllib.parse import urljoin, urlparse
import os
from bs4 import BeautifulSoup
from page_loader.content_actions import render_name, \
     make_request, download_files, save_to_file
import logging
import re


def process_main_page(url, work_dir):
    page_data = make_request(url).text
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    soup = BeautifulSoup(page_data, 'html.parser')
    links_to_download = process_soup(soup, url, work_dir)
    save_to_file(soup.prettify(), file_path, mode='w')
    errors = download_files(url, work_dir, links_to_download)
    if errors:
        pass
    else:
        logging.info(f"Page was successfully downloaded as '{file_path}'")
    return file_path


def get_key_from_tag(tag):
    for i in ('href', 'src'):
        if tag.get(i):
            return i
    return


def process_soup(soup, url, work_dir):
    links_to_download = []
    subdir_name = render_name(url, 'subdir')
    subdir_full_path = os.path.join(work_dir, subdir_name)
    logging.debug('------ analyzing page data ------')
    for obj in ('img', 'link', 'script'):
        logging.debug(f'* process <{obj}> tag *')
        tags = soup.findAll(obj)
        for tag in tags:
            key = get_key_from_tag(tag)
            if key:
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
    elif obj_url.netloc == source_url.netloc \
            or re.match(rf"^\w*\.{source_url.netloc}$", obj_url.netloc):
        return obj_href
    return
