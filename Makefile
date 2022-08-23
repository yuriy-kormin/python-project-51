install:
	poetry install

package-install:
	pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 pageloader

build:
	poetry build

test:
	poetry run pytest

coverage:
	poetry run pytest --cov=pageloader --cov-report xml tests/
