import os
import requests
# from pageloader.parser import render_name


def download_file(url, subdir_name, filename):
    file_path = os.path.join(subdir_name, filename)
    request = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        f.write(request.content)
    return file_path
