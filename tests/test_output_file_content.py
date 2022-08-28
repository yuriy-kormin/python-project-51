import tempfile
from urllib.parse import urljoin
from pageloader import download
import os


def read_file(path):
    with open(path, 'r') as f:
        result_content = f.read()
    return result_content


def test_result_html(test_url, test_filename,
                     simple_html_content, requests_mock):
    requests_mock.get(test_url, text=simple_html_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        result_path = download(test_url, tmpdir)
        assert read_file(result_path) == simple_html_content


def test_content_css(test_url, test_subdir_name, css_content,
                     simple_html_content, page_with_other_link,
                     requests_mock, test_css_filename, test_relative_filename):
    requests_mock.get(test_url, text=page_with_other_link)
    requests_mock.get(urljoin(test_url, 'inner'), text=simple_html_content)
    requests_mock.get(urljoin(test_url, 'css.css'), text=css_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        download(test_url, tmpdir)
        path = os.path.join(tmpdir, test_subdir_name, test_relative_filename)
        assert read_file(path) == simple_html_content
        path = os.path.join(tmpdir, test_subdir_name, test_css_filename)
        assert read_file(path) == css_content
