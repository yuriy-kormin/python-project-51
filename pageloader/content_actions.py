from urllib.parse import urlparse

import re
import os
import requests
from progress.bar import Bar


def download_files(urls):
    with Bar('Downloading', max=len(urls), suffix='%(percent)d%%') as bar:
        for url, path in urls:
            bar.next()
            request = requests.get(url, stream=True)
            with open(path, 'wb') as f:
                f.write(request.content)


def make_subdir(url, path):
    name = render_name(url, 'subdir')
    subdir_path = os.path.join(path, name)
    os.makedirs(subdir_path, exist_ok=True)
    return subdir_path


def replace_symbols(data):
    return re.sub(r'[^\da-zA-Z]', '-', data)


def render_name(url, output_type):
    url_data = url_parse(url)
    if output_type == 'html':
        return f"{url_data['loc']}{url_data['path']}.html"
    elif output_type == 'subdir':
        return f"{url_data['loc']}{url_data['path']}_files"
    elif output_type == 'file':
        name, ext = os.path.splitext(url_data['full_path'])
        name = replace_symbols(name)
        if not ext:
            ext = '.html'
        return f"{url_data['loc']}{name}{ext}"


def url_parse(url):
    url_parsed = urlparse(url)
    return {'loc': replace_symbols(url_parsed.netloc),
            'path': replace_symbols(os.path.splitext(url_parsed.path)[0]),
            'full_path': url_parsed.path
            }
