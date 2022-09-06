import os
from bs4 import BeautifulSoup
from page_loader.analize_content import process_links
import logging


def parse_page(url, file_path):
    workdir_name, _ = os.path.split(file_path)
    logging.debug(f'parsing html {file_path}')
    try:
        with open(file_path, 'r+') as f:
            file_data = f.read()
            logging.debug('file successfully read, processing to BS4')
            soup = BeautifulSoup(file_data, 'html.parser')
            logging.debug('file successfully parsed by BS4')
            process_links(soup, url, workdir_name)
            f.seek(0)
            logging.debug('try to write html after processing links')
            f.write(soup.prettify())
            logging.info(f"Page was successfully downloaded as '{file_path}'")
    except (FileNotFoundError, PermissionError):
        logging.exception(f'Cannot parse file {file_path}',
                          exc_info=True)
        raise
