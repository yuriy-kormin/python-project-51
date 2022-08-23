import pytest

TEST_URL = 'https://ru.hexlet.io/courses'
TEST_FILENAME = 'ru-hexlet-io-courses.html'


@pytest.fixture
def test_url():
    return TEST_URL


@pytest.fixture
def test_filename(test_url):
    return TEST_FILENAME
