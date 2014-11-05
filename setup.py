from setuptools import setup, find_packages
from os.path import join, dirname
from app import __version__

setup(
    name='sleekstatus',
    version=__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    install_requires = [
        'Flask==0.10.1',
        'redis==2.10.3'
        ],
)
