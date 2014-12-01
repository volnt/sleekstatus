all: pylint pep8 tests

tests:
	pip install -e .
	py.test --cov app --cov-report html tests/ 

pep8:
	pep8 app

pylint:
	pylint app

.PHONY: tests
