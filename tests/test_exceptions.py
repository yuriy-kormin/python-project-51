import os
from pageloader import download
import tempfile
import pytest


def test_isset_output_dir(test_url):
    with pytest.raises(FileNotFoundError):
        download(test_url, 'test_path')


def test_permissons(test_url):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'test_dir')
        os.mkdir(path, 0o444)
        with pytest.raises(PermissionError):
            download(test_url, path)
