from page_loader import download
import tempfile
import os
import pytest
import requests_mock
import requests


def test_write_output_path(url):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'test_dir')
        with pytest.raises(FileNotFoundError):
            download(url, path)
        os.mkdir(path, 0o444)
        with pytest.raises(PermissionError):
            download(url, path)


def test_invalid_url(url):
    with requests_mock.Mocker() as mock:
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              url,
                              exc=requests.exceptions.URLRequired)
            download(url)
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              url,
                              exc=requests.exceptions.ConnectionError)
            download(url)
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              url,
                              exc=requests.exceptions.TooManyRedirects)
            download(url)
        with pytest.raises(IOError):
            mock.register_uri('GET',
                              url,
                              exc=requests.exceptions.Timeout)
            download(url)


def test_wrong_link(url, html_with_links):
    with tempfile.TemporaryDirectory() as tmpdir, \
            requests_mock.Mocker() as mock:
        mock.get(requests_mock.ANY, text='')
        mock.get(url, text=html_with_links)
        mock.get('/data/file.png', status_code=404)
        download(url, tmpdir)
