import os
import tempfile
from pageloader import download
import filetype


def test_corrected_downloading(test_url, test_filename, requests_mock, image_path,
                               html_content_with_img_link, test_subdir_name):
    with tempfile.TemporaryDirectory() as tmpdir, open(image_path, 'rb') as f:
        requests_mock.get(test_url, text=html_content_with_img_link)
        requests_mock.get('https://hexlet.io/python.png', content=f.read())
        download(test_url, tmpdir)
        subdir_path = os.path.join(tmpdir, test_subdir_name, 'hexlet-io-python.png')
        with open(subdir_path, 'rb') as download_image, open(image_path,'rb') as source_image:
            download_image_data = download_image.read()
            source_image_data = source_image.read()
        assert filetype.is_image(subdir_path)
    assert download_image_data == source_image_data
