import pytest
import os

FIXTURES_PATH = 'fixtures'
TEST_URL = 'https://ru.hexlet.io/courses'
TEST_FILENAME = 'ru-hexlet-io-courses.html'
TEST_SUBDIR_NAME = 'ru-hexlet-io_files'


@pytest.fixture
def test_url():
    return TEST_URL


@pytest.fixture
def test_filename():
    return TEST_FILENAME


@pytest.fixture
def test_subdir_name():
    return TEST_SUBDIR_NAME


@pytest.fixture
def simple_html_content(fixtures_path):
    html_path = os.path.join(fixtures_path, 'simple.html')
    return read_file(html_path)


@pytest.fixture
def html_content_with_img_link(fixtures_path):
    html_path = os.path.join(fixtures_path, 'with_image_link.html')
    return read_file(html_path)


@pytest.fixture
def image_path(fixtures_path):
    return os.path.join(fixtures_path, 'python.png')


@pytest.fixture
def fixtures_path():
    return os.path.join(os.path.dirname(__file__), FIXTURES_PATH)


def read_file(path):
    with open(path, 'r') as f:
        result = f.read()
    return result
