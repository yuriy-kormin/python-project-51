import os
from pageloader import download
import tempfile
import pytest


def test_isset_output_dir(test_url):
    with pytest.raises(SystemExit) as e:
        download(test_url, 'test_path')
    assert e.value.code == 0

