import os
import requests


def download(address, path = None):
    if path is None:
        path = os.getcwd()
    request = requests.get(address)
    return request.text
