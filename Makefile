test:
	pip install -e .
	py.test --cov app --cov-report html tests/ 
