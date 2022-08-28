import os
import tempfile
from pageloader import download
import filetype


def test_corrected_downloading(test_url, test_filename,
                               requests_mock, image_path,
                               html_content_with_img_link, test_subdir_name):
    with tempfile.TemporaryDirectory() as tmpdir, open(image_path, 'rb') as f:
        requests_mock.get(test_url, text=html_content_with_img_link)
        image_data = f.read()
        requests_mock.get('https://ru.hexlet.io/python.png',
                          content=image_data)
        requests_mock.get('https://cdn2.hexlet.io/python.png',
                          content=image_data)
        download(test_url, tmpdir)
        download_image_path = os.path.join(tmpdir,
                                           test_subdir_name,
                                           'ru-hexlet-io-python.png')
        assert os.path.isfile(download_image_path)
        passed_image_path = os.path.join(
            tmpdir, test_subdir_name, 'cdn2-hexlet-io-python.png')
        assert not os.path.exists(passed_image_path)
        with open(download_image_path, 'rb') as download_image, \
                open(image_path, 'rb') as source_image:
            download_image_data = download_image.read()
            source_image_data = source_image.read()
        assert filetype.is_image(download_image_path)
        assert download_image_data == source_image_data

#
# def test_other_link(test_url,page_with_other_link,requests_mock,test_subdir_name):
#     requests_mock.get(test_url, text=page_with_other_link)
#     requests_mock.get()