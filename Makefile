install:
	poetry install

package-install:
	pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_loader tests

build:
	poetry build

test:
	poetry run pytest --ignore=tests_old -s

coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/
