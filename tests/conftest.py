import pytest
import os

FIXTURES_PATH = 'fixtures'
TEST_URL = 'https://ru.hexlet.io/courses'
TEST_FILENAME = 'ru-hexlet-io-courses.html'
TEST_SUBDIR_NAME = 'ru-hexlet-io-courses_files'
TEST_RELATIVE_FILENAME = 'ru-hexlet-io-inner.htm'
TEST_CSS_FILENAME = 'ru-hexlet-io-css.css'


@pytest.fixture
def test_url():
    return TEST_URL


@pytest.fixture
def test_filename():
    return TEST_FILENAME


@pytest.fixture
def test_relative_filename():
    return TEST_RELATIVE_FILENAME


@pytest.fixture
def test_css_filename():
    return TEST_CSS_FILENAME


@pytest.fixture
def test_subdir_name():
    return TEST_SUBDIR_NAME


@pytest.fixture
def page_with_other_link(fixtures_path):
    return read_file(os.path.join(fixtures_path, 'with_other_link.html'))


@pytest.fixture
def simple_html_content(fixtures_path):
    html_path = os.path.join(fixtures_path, 'simple.html')
    return read_file(html_path)


@pytest.fixture
def css_content(fixtures_path):
    css_path = os.path.join(fixtures_path, 'css.css')
    return read_file(css_path)


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
