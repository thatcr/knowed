try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'knowed - python data dependency framework',
    'author': 'Rob Thatcher',
    'author_email': 'thatcr@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['knowed'],
    'scripts': [],
    'name': 'knowed'
}

setup(**config)