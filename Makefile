.PHONY: virtualenv install pflake8 test

virtualenv:
	pip install --user pipenv
	pipenv shell

install:
	@echo "Hidded Installing..."
	echo "Installing..."
	pipenv install

lint:
	pflake8

format:
	isort logic migrations persistency routers tests utils
	black logic migrations persistency routers tests utils

test:
	pytest -s
