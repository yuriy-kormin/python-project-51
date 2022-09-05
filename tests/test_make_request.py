import tempfile
from page_loader import download


def test_request(test_url, test_filename, requests_mock):
    req_mock = requests_mock.get(test_url)
    with tempfile.TemporaryDirectory() as tmpdir:
        download(test_url, tmpdir)
    assert req_mock.call_count == 1
