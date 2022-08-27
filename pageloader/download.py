import re
import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def download(address, path=None):
    if path is None:
        path = os.getcwd()
    request = requests.get(address)
    file_path = os.path.join(path, render_name(address, 'html'))
    save_to_file(request.text, file_path)
    subdir_name = make_subdir(address, path)
    parse_html(address, file_path, subdir_name)
    return file_path


def parse_html(src_address, file_path, subdir_name):
    result = ''
    with open(file_path, 'r+') as f:
        file_data = f.read()
        soup = BeautifulSoup(file_data, 'html.parser')
        process_img_src(soup, src_address, subdir_name)
        process_other_src(soup, src_address, subdir_name)
        f.seek(0)
        f.write(soup.prettify())
    return result


def process_other_src(soup, src_address, subdir):
    for tag_name in ('link', 'script'):
        tags = soup.findAll(tag_name, {'href': True})
        for tag in tags:
            if need_to_download(src_address, tag['href']):
                tag['href'] = download_file(tag['href'], subdir)


def process_img_src(soup, src_address, subdir):
    tags = soup.findAll('img')
    for tag in tags:
        if need_to_download(src_address, tag['src']):
            tag['src'] = download_file(tag['src'], subdir)


def need_to_download(src_address, obj_href):
    source_url, img_url = map(url_parse, (src_address, obj_href))
    print(obj_href)
    _, ext = os.path.splitext(img_url['full_path'])
    if img_url['loc'] == source_url['loc'] and len(ext) > 0:
        return True


def download_file(address, subdir_name):
    file_path = os.path.join(subdir_name, render_name(address, 'file_name'))
    request = requests.get(address, stream=True)
    save_to_file(request.content, file_path, binary=True)
    return file_path


def make_subdir(address, path):
    name = render_name(address, 'subdir')
    subdir_path = os.path.join(path, name)
    os.makedirs(subdir_path, exist_ok=True)
    return subdir_path


def render_name(address, output_type):
    url = url_parse(address)
    if output_type == 'html':
        return f"{url['loc']}{url['path']}.html"
    elif output_type == 'subdir':
        return f"{url['loc']}_files"
    elif output_type == 'file_name':
        name, ext = os.path.splitext(url['full_path'])
        name = replace_symbols(name)
        return f"{url['loc']}{name}{ext}"


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
