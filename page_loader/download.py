import os
from page_loader.analize_content import parse_page, process_soup
from page_loader.content_actions import render_name, save_to_file, \
    make_request, download_files
from page_loader.logger import setup_logger
import logging


def download(url, output=None):
    work_dir = output if output else os.getcwd()
    setup_logger()
    logging.info(f'requested url: {url}')
    logging.info(f'output path:  {work_dir}')
    return process_main_page(url, work_dir)


def process_main_page(url, work_dir):
    file = download_main_page(url, work_dir)
    updated_html_data = process_content(url, file)
    logging.debug('try to write html after processing links')
    save_to_file(updated_html_data, file, mode='w')
    logging.info(f"Page was successfully downloaded as '{file}'")
    return file


def download_main_page(url, work_dir):
    file_path = os.path.join(work_dir, render_name(url, 'html'))
    request = make_request(url)
    save_to_file(request.text, file_path, mode='w')
    return file_path


def process_content(url, file_name):
    work_dir, _ = os.path.split(file_name)
    soup = parse_page(file_name)
    links_to_download = process_soup(soup, url, work_dir)
    download_files(url, work_dir, links_to_download)
    return soup.prettify()
