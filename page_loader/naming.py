import logging
import os
import re
from urllib.parse import urlparse


def render_name(url, output_type):
    logging.debug(f'rendering name for {url}')
    url_parsed = urlparse(url)
    loc = formatter(url_parsed.netloc)
    path, ext = os.path.splitext(url_parsed.path)
    formatted_path = formatter(path)
    if output_type == 'html':
        return f"{loc}{formatted_path}.html"
    elif output_type == 'subdir':
        return f"{loc}{formatted_path}_files"
    elif output_type == 'file':
        if not ext:
            ext = '.html'
        return f"{loc}{formatted_path}{ext}"


def formatter(data):
    return re.sub(r'[^\da-zA-Z]', '-', data)
