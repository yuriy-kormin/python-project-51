import requests


def download_files(urls):
    for url, path in urls:
        request = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            f.write(request.content)
