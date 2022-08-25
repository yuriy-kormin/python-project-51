import os
import tempfile
from pageloader import download


def test_result_html(test_url, test_filename, simple_html_content, requests_mock):
    req_mock = requests_mock.get(test_url, text=simple_html_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        result_path = download(test_url, tmpdir)
        result_html_path = os.path.join(result_path, test_filename)
        with open(result_path, 'r') as f:
            result_html_content = f.read()
    assert result_html_content == simple_html_content
