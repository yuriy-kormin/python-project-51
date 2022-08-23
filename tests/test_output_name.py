import os
import tempfile
import pook
from pageloader import download


@pook.on
def test_result_file(test_url, test_filename):
    pook.get(test_url)
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_file = os.path.join(tmpdirname, test_filename)
        assert download(test_url, tmpdirname) == test_file
        assert os.path.exists(test_file)
