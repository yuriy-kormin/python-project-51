import os
import tempfile
from re import search
from pageloader import download


def read_file(path):
    with open(path, 'r') as f:
        result_content = f.read()
    return result_content


def test_log_isset(test_url, simple_html_content, requests_mock):
    requests_mock.get(test_url, text=simple_html_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        download(test_url, tmpdir)
        log_path = os.path.join(tmpdir, 'log')
        assert os.path.isfile(log_path)


def test_log_content(test_url, simple_html_content, test_filename,
                     requests_mock):
    requests_mock.get(test_url, text=simple_html_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        download(test_url, tmpdir)
        log_path = os.path.join(tmpdir, 'log')
        log_content = read_file(log_path)
        assert search(fr'{test_url}\n', log_content)
        assert search(fr'{tmpdir}\n', log_content)
        assert search(fr'{test_filename}\n', log_content)
