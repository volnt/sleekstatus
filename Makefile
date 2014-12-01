all: install pylint pyflakes pep8 tests

install:
	pip install -e .

tests:
	py.test --cov app --cov-report html tests/ 

pep8:
	pep8 app

pyflakes:
	pyflakes app

pylint:
	pylint --disable=deprecated-module --disable=no-member --disable=cyclic-import --disable=too-many-arguments --const-rgx='[A-Za-z0-9_]{2,30}$$' app/

.PHONY: all install tests pep8 pyflakes pylint
