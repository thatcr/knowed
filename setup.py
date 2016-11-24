
from setuptools import setup, find_packages

config = {
    'description': 'Area 51 - Where they hide all the UFOs',
    'author': 'Rob Thatcher',
    'author_email': 'thatcr@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'package_dir': {'': 'src'},
    'packages': find_packages('src'),
    'scripts': [],
    'name': 'area51'
}

setup(**config)