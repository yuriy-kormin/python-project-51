import os
import tempfile
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
