from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='sleekstatus',
    version="0.1.1",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    install_requires = [
        'Flask==0.10.1',
        'redis==2.10.3',
        'stripe==1.19.1',
        'celery==3.1.17',
        'boto==2.34.0'
        ],
)
