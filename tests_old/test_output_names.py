import tempfile
from page_loader import download
import os
from urllib.parse import urljoin


def test_name_html_file(test_url, test_filename, page_with_other_link,
                        test_subdir_name, requests_mock):
    test_url_ext = f'{test_url}.mht'
    requests_mock.get(test_url_ext, text=page_with_other_link)
    requests_mock.get(urljoin(test_url, 'inner'), text=page_with_other_link)
    requests_mock.get(urljoin(test_url, 'css.css'), text=page_with_other_link)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, test_filename)
        assert download(test_url_ext, tmpdir) == test_file
        assert os.path.exists(test_file)
        assert os.path.exists(os.path.join(tmpdir, test_subdir_name))


def test_sublink_path(test_url, test_subdir_name, css_content,
                      simple_html_content, page_with_other_link,
                      requests_mock, test_css_filename,
                      test_relative_filename):
    requests_mock.get(test_url, text=page_with_other_link)
    requests_mock.get(urljoin(test_url, 'inner'), text=simple_html_content)
    requests_mock.get(urljoin(test_url, 'css.css'), text=css_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        download(test_url, tmpdir)
        for filename in (test_relative_filename, test_css_filename):
            file_path = os.path.join(tmpdir, test_subdir_name, filename)
            assert os.path.isfile(file_path)
