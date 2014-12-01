all: pyflakes pep8 tests

tests:
	pip install -e .
	py.test --cov app --cov-report html tests/ 

pep8:
	pep8 app

pyflakes:
	pyflakes app

.PHONY: tests
