import os.path

import pytest

FIXTURES_PATH = 'fixtures'
TEST_URL = 'https://subdomain.domain.com/subdir'
TEST_FILENAME = 'subdomain-domain-com-subdir.html'
TEST_SUBDIR_NAME = 'subdomain-domain-com-subdir_files'


def read_file(path):
    with open(path, 'r') as f:
        result = f.read()
    return result


@pytest.fixture
def fixtures_path():
    return os.path.join(os.path.dirname(__file__), FIXTURES_PATH)


@pytest.fixture
def url():
    return TEST_URL


@pytest.fixture
def output_html_name():
    return TEST_FILENAME


@pytest.fixture
def subdir_name():
    return TEST_SUBDIR_NAME


@pytest.fixture
def html(fixtures_path):
    path = os.path.join(fixtures_path, 'simple_without_links.html')
    return read_file(path)


@pytest.fixture
def html_with_links(fixtures_path):
    path = os.path.join(fixtures_path, 'with_inner_links.html')
    return read_file(path)


@pytest.fixture
def subdir_filenames():
    return [
        'subdomain-domain-com-another.html',
        'subdomain-domain-com-data-file.png',
        'subdomain-domain-com-script.js',
        'subdomain-domain-com-simple.html'
    ]
