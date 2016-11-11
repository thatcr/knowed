try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Area 51 - Where they hide all the UFOs',
    'author': 'Rob Thatcher',
    'author_email': 'thatcr@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['src/area51'],
    'scripts': [],
    'name': 'area51'
}

setup(**config)