from urllib.parse import urljoin
import os
from page_loader.content_actions import download_files, make_subdir, \
    render_name, url_parse
import logging


def process_links(soup, url, workdir):
    links = []
    subdir_name = render_name(url, 'subdir')
    subdir = os.path.join(workdir, subdir_name)
    for obj in ('img', 'link', 'script'):
        key = 'src' if obj == 'img' else 'href'
        logging.debug(f'-------process tag------- <{obj}>')
        tags = soup.findAll(obj, {key: True})
        for tag in tags:
            logging.debug(f'processing {tag[key]}')
            obj_url = need_to_download(url, tag[key])
            if obj_url:
                logging.debug(f' + need to download {tag[key]}')
                file_name = render_name(obj_url, 'file')
                local_path = os.path.join(subdir, file_name)
                links.append((obj_url, local_path))
                tag[key] = local_path
            else:
                logging.debug(f' - pass {tag[key]}')
        if not len(tags):
            logging.debug(' - nothing to process -')
    if len(links):
        make_subdir(subdir)
        download_files(links)


def need_to_download(url: str, obj_href: str) -> str:
    """ Check that address and  href on the same domain name and
    must be downloaded. return link to download file or None if
    file will not be downloaded"""
    source_url, obj_url = map(url_parse, (url, obj_href))
    if not obj_url['loc']:
        return urljoin(url, obj_href)
    _, ext = os.path.splitext(obj_url['full_path'])
    if obj_url['loc'] == source_url['loc']:
        return obj_href
    return
