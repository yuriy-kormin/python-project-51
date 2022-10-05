import os
import requests
from progress.bar import Bar
from page_loader.fs import check_dir, save_to_file, make_subdir
from page_loader.html import process_html
from page_loader.naming import render_name
from page_loader.logger import setup_logger
import logging


def download(url, output=None):
    setup_logger()
    work_dir = output if output else os.getcwd()
    check_dir(work_dir)
    logging.info(f'requested url: {url}')
    logging.info(f'output path:  {work_dir}')
    page_data = make_request(url).text
    processed_html, downloads = process_html(page_data, url, work_dir)
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    save_to_file(processed_html, file_path, mode='w')
    if downloads:
        make_subdir(url, work_dir)
    errors = download_files(downloads)
    if errors:
        error_str = "\n    ".join(errors)
        logging.info(
            f'Page was partially downloaded, some errors occur: \n{error_str}')
    else:
        logging.info(f"Page was successfully downloaded as '{file_path}'")
    return file_path


def download_files(links_to_download):
    errors = []
    logging.debug('------ downloading content ------')
    with Bar('Downloading', max=len(links_to_download),
             suffix='%(percent)d%%') as bar:
        for url, path in links_to_download:
            logging.debug(f'process url: {url}')
            try:
                data = make_request(url).content
            except Exception as e:
                data = b''
                errors.append(str(e))
                logging.debug(f'error raised\n{e}')
            else:
                bar.next()
            finally:
                save_to_file(data, path)
    return errors


def make_request(url):
    logging.debug('making request...')
    request = requests.get(url, stream=True)
    if request.status_code != 200:
        logging.debug(f'cannot fetch {url}')
        request.raise_for_status()
    return request
