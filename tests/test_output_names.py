import os
import tempfile
import pook
from pageloader import download


@pook.on
def test_result_file(test_url, test_filename, test_subdir_name):
    test_url_ext = f'{test_url}.mht'
    pook.get(test_url_ext)
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_file = os.path.join(tmpdirname, test_filename)
        assert download(test_url_ext, tmpdirname) == test_file
        assert os.path.exists(test_file)
        assert os.path.exists(os.path.join(tmpdirname, test_subdir_name))
