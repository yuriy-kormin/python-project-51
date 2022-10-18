import logging
import os
import re
from typing import Dict
from urllib.parse import urlparse


def render_subdir_name(url: str) -> str:
    logging.debug(f'rendering subdir name for {url}')
    url_parsed = urlparse(url)
    path, _ = os.path.splitext(url_parsed.path)
    loc, path = map(formatter, (url_parsed.netloc, path))
    return f'{loc}{path}_files'


def render_filename(url: str) -> str:
    logging.debug(f'rendering name for {url}')
    url_parsed = urlparse(url)
    path, ext = os.path.splitext(url_parsed.path)
    if not ext:
        ext = '.html'
    loc, path = map(formatter, (url_parsed.netloc, path))
    return f'{loc}{path}{ext}'


def formatter(data: str) -> str:
    return re.sub(r'[^\da-zA-Z]', '-', data)
