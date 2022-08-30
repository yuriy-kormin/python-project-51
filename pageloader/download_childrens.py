import requests
from progress.bar import Bar


def download_files(urls):
    with Bar('Downloading', max=len(urls), suffix='%(percent)d%%') as bar:
        for url, path in urls:
            bar.next()
            request = requests.get(url, stream=True)
            with open(path, 'wb') as f:
                f.write(request.content)
