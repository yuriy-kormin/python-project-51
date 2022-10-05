import filetype

from page_loader import download
import tempfile
import os
import requests_mock


def test_html_file_isset(html, url, output_html_name, subdir_name):
    with tempfile.TemporaryDirectory() as tmpdir, \
            requests_mock.Mocker() as mock:
        mock.get(url, text=html)
        output_html = os.path.join(tmpdir, output_html_name)
        subdir = os.path.join(tmpdir, subdir_name)
        assert download(url, tmpdir) == output_html
        assert not os.path.exists(subdir)
        assert mock.call_count == 1


def test_create_subdir_download_files(
        url, html_with_links, subdir_name, subdir_filenames):
    with tempfile.TemporaryDirectory() as tmpdir, \
            requests_mock.Mocker() as mock:
        subdir = os.path.join(tmpdir, subdir_name)
        mock.get(requests_mock.ANY,
                 text='')
        mock.get(url, text=html_with_links)
        download(url, tmpdir)
        assert os.path.isdir(subdir)
        files = os.listdir(subdir)
        files.sort()
        assert files == subdir_filenames


def test_html_modifying(url, html_with_links, subdir_name, subdir_filenames):
    with tempfile.TemporaryDirectory() as tmpdir, \
            requests_mock.Mocker() as mock:
        mock.get(requests_mock.ANY,
                 text='')
        mock.get(url, text=html_with_links)
        filepath = download(url, tmpdir)
        html_data = open(filepath, 'r').read()
        for filename in subdir_filenames:
            filepath = os.path.join(subdir_name, filename)
            assert filepath in html_data


def test_subfiles_data(
        url, subfiles_data, html_with_links, subdir_name):
    with tempfile.TemporaryDirectory() as tmpdir, \
            requests_mock.Mocker() as mock:
        mock.get(requests_mock.ANY,
                 text='')
        mock.get(url, text=html_with_links)
        mock.get('/data/file.png', content=subfiles_data['png'])
        mock.get('/script.js', text=subfiles_data['js'])
        download(url, tmpdir)
        image_path = os.path.join(
            tmpdir, subdir_name, 'subdomain-domain-com-data-file.png')
        js_path = os.path.join(
            tmpdir, subdir_name, 'subdomain-domain-com-script.js')
        assert filetype.is_image(image_path)
        assert open(js_path, 'r').read() == subfiles_data['js']
