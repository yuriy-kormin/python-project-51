from urllib.parse import urljoin
import os
from bs4 import BeautifulSoup
from page_loader.content_actions import render_name, \
    url_parse, make_request, download_files, save_to_file
import logging
import re


def process_main_page(url, work_dir):
    page_data = make_request(url).text
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    soup = BeautifulSoup(page_data, 'html.parser')
    links_to_download = process_soup(soup, url, work_dir)
    download_files(url, work_dir, links_to_download)
    save_to_file(soup.prettify(), file_path, mode='w')
    logging.info(f"Page was successfully downloaded as '{file_path}'")
    return file_path


def process_soup(soup, url, work_dir):
    links_to_download = []
    subdir_name = render_name(url, 'subdir')
    subdir = os.path.join(work_dir, subdir_name)
    logging.debug('------ analyzing page data ------')
    for obj in ('img', 'link', 'script'):
        key = 'src' if obj == 'img' else 'href'
        logging.debug(f'* process <{obj}> tag *')
        tags = soup.findAll(obj, {key: True})
        for tag in tags:
            obj_url = need_to_download(url, tag[key])
            if obj_url:
                logging.debug(f' + {tag[key]}')
                file_name = render_name(obj_url, 'file')
                local_path = os.path.join(subdir, file_name)
                links_to_download.append((obj_url, local_path))
                tag[key] = local_path
            else:
                logging.debug(f' - {tag[key]}')
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
    elif obj_url['netloc'] == source_url['netloc'] or \
            re.match(rf"^\w*\.{source_url['netloc']}$", obj_url['netloc']):
        return obj_href
    return
