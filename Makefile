all: install pylint pyflakes pep8 tests

install:
	pip install -e .

tests:
	py.test --cov app --cov-report html tests/ 
	jasmine-ci

pep8:
	pep8 app

pyflakes:
	pyflakes app

pylint:
	pylint --disable=deprecated-module --disable=no-member --disable=cyclic-import --disable=too-many-arguments --const-rgx='[A-Za-z0-9_]{2,30}$$' app/

release: sleekstatus-env.zip

sleekstatus-env.zip: /tmp/sleek-release /tmp/sleek-release/config.py
	cd /tmp/sleek-release && zip -r $@ Dockerfile Dockerrun.aws.json config.py sleekstatus
	cp /tmp/sleek-release/$@ $@

/tmp/sleek-release:
	rm -rf $@
	mkdir $@
	cd $@ && git clone git@github.com:volnt/sleekstatus.git
	cd $@ && cp sleekstatus/Docker* .
	cd $@/sleekstatus/app/static/ && compass compile

/tmp/sleek-release/config.py:
	@rm -f $@
	@echo "AWS = {" >> $@
	@echo "    'ACCESS_KEY_ID': $(AWS_ACCESS_KEY_ID)," >> $@
	@echo "    'SECRET_ACCESS_KEY': $(AWS_SECRET_ACCESS_KEY)" >> $@
	@echo "}" >> $@

.PHONY: all install tests pep8 pyflakes pylint release
