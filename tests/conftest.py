import pytest

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
