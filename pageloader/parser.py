import os
from bs4 import BeautifulSoup
from pageloader.analize_content import process_links
from pageloader.logger import get_logger


def parse_html(url, file_path):
    dir_name, _ = os.path.split(file_path)
    log = get_logger(__name__, os.path.join(dir_name, 'log'))
    log.debug(f'parsing html {file_path}')
    result = ''
    with open(file_path, 'r+') as f:
        file_data = f.read()
        soup = BeautifulSoup(file_data, 'html.parser')
        process_links(soup, url, dir_name)
        f.seek(0)
        f.write(soup.prettify())
    return result
