import os
import tempfile
import pook
from pageloader import download


@pook.on
def test_result_file(test_url, test_filename):
    test_file_data = '<HTML> HELLO! ITs a test html</HTML>'
    pook.get(test_url, response_json={'body': test_file_data})
    with tempfile.TemporaryDirectory() as tmpdirname:
        download(test_url, tmpdirname)
        f = open(os.path.join(tmpdirname, test_filename), 'r')
        file_data = f.readlines()
        assert file_data == ['{\n', f'    "body": "{test_file_data}"\n', '}']
