import os
from page_loader import download
import tempfile
import pytest
import requests
import requests_mock


def test_isset_output_dir(test_url):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'test_dir')
        with pytest.raises(FileNotFoundError):
            download(test_url, path)


def test_permissons(test_url):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'test_dir')
        os.mkdir(path, 0o444)
        with pytest.raises(PermissionError):
            download(test_url, path)


def test_invalid_url(test_url):
    with requests_mock.Mocker() as mock:
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              test_url,
                              exc=requests.exceptions.URLRequired)
            download(test_url)
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              test_url,
                              exc=requests.exceptions.ConnectionError)
            download(test_url)
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              test_url,
                              exc=requests.exceptions.TooManyRedirects)
            download(test_url)
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              test_url,
                              exc=requests.exceptions.Timeout)
            download(test_url)


def test_wrong_link(test_url, html_content_with_img_link, requests_mock):
    requests_mock.get(test_url, text=html_content_with_img_link)
    # requests_mock.get('https://ru.hexlet.io/python.png', status_code=404)
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(requests.exceptions.HTTPError):
            download(test_url, tmpdir)
