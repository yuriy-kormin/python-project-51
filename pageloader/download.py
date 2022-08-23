import re
import os
import requests


def download(address, path=None):
    if path is None:
        path = os.getcwd()
    request = requests.get(address)
    path = os.path.join(path, render_html_filename(address))
    save_to_file(request.text, path)
    return path


def render_html_filename(address):
    filename = re.sub(r'(^https?:\/\/|\.[a-zA-Z]+$)', '', address)
    filename = re.sub(r'[^\da-zA-Z]', '-', filename)
    return f'{filename}.html'


def save_to_file(data, path):
    with open(path, "w") as f:
        f.write(data)
