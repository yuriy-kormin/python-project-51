import tempfile
import pook
from pageloader import download


@pook.on
def test_request(test_url, test_filename):
    mock = pook.get(test_url)
    with tempfile.TemporaryDirectory() as tmpdirname:
        download(test_url, tmpdirname)
        assert mock.calls == 1
