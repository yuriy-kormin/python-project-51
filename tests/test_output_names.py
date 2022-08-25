import os
import tempfile
from pageloader import download


def test_name_html_file(test_url, test_filename,
                        test_subdir_name, requests_mock):
    test_url_ext = f'{test_url}.mht'
    requests_mock.get(test_url_ext)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, test_filename)
        assert download(test_url_ext, tmpdir) == test_file
        assert os.path.exists(test_file)
        assert os.path.exists(os.path.join(tmpdir, test_subdir_name))
