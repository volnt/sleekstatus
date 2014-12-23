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


major: sleekstatus-env.zip
	@printf "Deploying major version ............\n"
	@python deploy.py --major -v
	@rm sleekstatus-env.zip
	@rm -rf /tmp/sleek-release

minor: sleekstatus-env.zip
	@printf "Deploying minor version ............\n"
	@python deploy.py --minor -v
	@rm sleekstatus-env.zip
	@rm -rf /tmp/sleek-release

fix: sleekstatus-env.zip
	@printf "Deploying fix version ..............\n"
	@python deploy.py --fix -v
	@rm sleekstatus-env.zip
	@rm -rf /tmp/sleek-release

sleekstatus-env.zip: /tmp/sleek-release /tmp/sleek-release/config.py
	@printf "Building sleekstatus.zip release ...\n"
	@cd /tmp/sleek-release && zip -r $@ *
	@cp /tmp/sleek-release/$@ $@

/tmp/sleek-release:
	@printf "Building release directory .........\n"
	@rm -rf $@
	@mkdir $@
	@cd $@ && git clone git@github.com:volnt/sleekstatus.git
	@cd $@ && cp sleekstatus/conf/* .
	@cd $@ && rm -rf sleekstatus/.git
	@cd $@/sleekstatus/app/static/ && compass compile

/tmp/sleek-release/config.py: /tmp/sleek-release
	@printf "Building config.py .................\n"
	@rm -f $@
	@echo "AWS = {" >> $@
	@echo "    'ACCESS_KEY_ID': '$(AWS_ACCESS_KEY_ID)'," >> $@
	@echo "    'SECRET_ACCESS_KEY': '$(AWS_SECRET_ACCESS_KEY)'" >> $@
	@echo "}" >> $@

.PHONY: all install tests pep8 pyflakes pylint release major fix minor
