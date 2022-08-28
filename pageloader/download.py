import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def download(address, path=None):
    if path is None:
        path = os.getcwd()
    request = requests.get(address)
    file_path = os.path.join(path, render_name(address, 'html'))
    save_to_file(request.text, file_path)
    subdir_name = make_subdir(address, path)
    parse_html(address, file_path, subdir_name)
    return file_path


def make_subdir(address, path):
    name = render_name(address, 'subdir')
    subdir_path = os.path.join(path, name)
    os.makedirs(subdir_path, exist_ok=True)
    return subdir_path


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


def save_to_file(data, path, binary=False):
    mode = 'wb' if binary else 'w'
    with open(path, mode) as f:
        f.write(data)


def parse_html(address, file_path, subdir_name):
    result = ''
    with open(file_path, 'r+') as f:
        file_data = f.read()
        soup = BeautifulSoup(file_data, 'html.parser')
        process_img_src(soup, address, subdir_name)
        process_other_src(soup, address, subdir_name)
        f.seek(0)
        f.write(soup.prettify())
    return result


def process_other_src(soup, address, subdir):
    for tag_name in ('link', 'script'):
        tags = soup.findAll(tag_name, {'href': True})
        for tag in tags:
            print(tag['href'])
            full_url = need_to_download(address, tag['href'])
            if full_url:
                print('downloading...')
                tag['href'] = download_file(full_url, subdir)


def process_img_src(soup, address, subdir):
    tags = soup.findAll('img')
    for tag in tags:
        url = need_to_download(address, tag['src'])
        if url:
            tag['src'] = download_file(url, subdir)


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


def download_file(url, subdir_name):
    file_path = os.path.join(subdir_name, render_name(url, 'file'))
    request = requests.get(url, stream=True)
    save_to_file(request.content, file_path, binary=True)
    return file_path
