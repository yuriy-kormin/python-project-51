import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pageloader.download_childrens import download_files


def need_to_download(address: str, obj_href: str) -> str:
    ''' Check that address and  href on the same domain name and
    must be downloaded. return link to download file or None '''
    source_url, obj_url = map(url_parse, (address, obj_href))
    if not obj_url['loc']:
        return urljoin(address, obj_href)
    _, ext = os.path.splitext(obj_url['full_path'])
    if obj_url['loc'] == source_url['loc']:
        return obj_href
    return


def process_links(soup, address, subdir):
    result = []
    for obj in ('img', 'link', 'script'):
        key = 'src' if obj == 'img' else 'href'
        tags = soup.findAll(obj, {key: True})
        for tag in tags:
            full_url = need_to_download(address, tag[key])
            if full_url:
                local_path = os.path.join(subdir, render_name(
                                                full_url, 'file'))
                result.append((full_url, local_path))
                tag[key] = local_path
    return result


def parse_html(address, file_path, subdir_name):
    result = ''
    with open(file_path, 'r+') as f:
        file_data = f.read()
        soup = BeautifulSoup(file_data, 'html.parser')
        to_download = process_links(soup, address, subdir_name)
        download_files(to_download)
        f.seek(0)
        f.write(soup.prettify())
    return result


def render_name(url, output_type):
    url_data = url_parse(url)
    if output_type == 'html':
        return f"{url_data['loc']}{url_data['path']}.html"
    elif output_type == 'subdir':
        return f"{url_data['loc']}_files"
    elif output_type == 'file':
        name, ext = os.path.splitext(url_data['full_path'])
        name = replace_symbols(name)
        if not ext:
            ext = '.html'
        return f"{url_data['loc']}{name}{ext}"


def replace_symbols(data):
    return re.sub(r'[^\da-zA-Z]', '-', data)


def url_parse(address):
    url = urlparse(address)
    return {'loc': replace_symbols(url.netloc),
            'path': replace_symbols(os.path.splitext(url.path)[0]),
            'full_path': url.path
            }
