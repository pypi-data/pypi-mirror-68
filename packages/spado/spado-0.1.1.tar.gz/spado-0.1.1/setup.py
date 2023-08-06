# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spado']
install_requires = \
['boto3>=1.13.8,<2.0.0']

setup_kwargs = {
    'name': 'spado',
    'version': '0.1.1',
    'description': 'Client simplifying and abstracting common operations for digital ocean spaces.',
    'long_description': None,
    'author': 'Alex Pedersen',
    'author_email': 'me@alexpdr.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
