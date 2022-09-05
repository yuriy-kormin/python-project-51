from urllib.parse import urljoin
import os
from page_loader.content_actions import download_files, make_subdir, \
    render_name, url_parse
import logging


def process_links(soup, url, dir_name):
    links = []
    subdir_created = False
    for obj in ('img', 'link', 'script'):
        key = 'src' if obj == 'img' else 'href'
        logging.debug(f'______\nprocess tag {obj}')
        tags = soup.findAll(obj, {key: True})
        for tag in tags:
            logging.debug(f'processing {tag[key]}')
            obj_url = need_to_download(url, tag[key])
            if obj_url:
                logging.debug(f' - need to download {tag[key]}')
                if not subdir_created:
                    subdir_created = True
                    logging.debug(f'making subdir {dir_name}')
                    subdir_path = make_subdir(url, dir_name)
                file_name = render_name(obj_url, 'file')
                local_path = os.path.join(subdir_path, file_name)
                links.append((obj_url, local_path))
                tag[key] = local_path
    if download_files(links):
        return True
    return


def need_to_download(url: str, obj_href: str) -> str:
    ''' Check that address and  href on the same domain name and
    must be downloaded. return link to download file or None '''
    source_url, obj_url = map(url_parse, (url, obj_href))
    if not obj_url['loc']:
        return urljoin(url, obj_href)
    _, ext = os.path.splitext(obj_url['full_path'])
    if obj_url['loc'] == source_url['loc']:
        return obj_href
    return
