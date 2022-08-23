import re
import os
import requests
from urllib.parse import urlparse


def download(address, path=None):
    if path is None:
        path = os.getcwd()
    request = requests.get(address)
    path = os.path.join(path, render_name(address, 'html'))
    save_to_file(request.text, path)
    make_dir(render_name(address, 'subdir'))
    return path


def make_dir(path):
    os.makedirs(path,exist_ok=True)


def render_name(address, output_type, link=None):
    url = url_parse(address)
    if output_type == 'html':
        return f"{url['loc']}{url['path']}.html"
    elif output_type == 'subdir':
        return f"{url['loc']}_files"
    elif link:
        return f"{url['loc']}-{replace_symbols(link)}"


def replace_symbols(data):
    return re.sub(r'[^\da-zA-Z]', '-', data)


def url_parse(address):
    url = urlparse(address)
    return {'loc': replace_symbols(url.netloc),
            'path': replace_symbols(os.path.splitext(url.path)[0])
            }


def save_to_file(data, path):
    with open(path, "w") as f:
        f.write(data)
