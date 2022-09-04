import os
from bs4 import BeautifulSoup
from pageloader.analize_content import process_links
import logging


def parse_page(url, file_path):
    dir_name, _ = os.path.split(file_path)
    logging.debug(f'parsing html {file_path}')
    try:
        with open(file_path, 'r+') as f:
            file_data = f.read()
            logging.debug('file successfully read, processing to BS4')
            soup = BeautifulSoup(file_data, 'html.parser')
            logging.debug('file successfully parsed be BS4')
            process_links(soup, url, dir_name)
            f.seek(0)
            try:
                logging.debug('try to write html after processing links')
                f.write(soup.prettify())
            except Exception:
                logging.exception('Cannot write file after processing links.',
                                  exc_info=True)
    except Exception:
        logging.exception(f'Cannot open file {file_path} for parsing',
                          exc_info=True)
