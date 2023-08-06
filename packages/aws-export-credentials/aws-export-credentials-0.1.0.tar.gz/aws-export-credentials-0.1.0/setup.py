# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_export_credentials']
install_requires = \
['botocore']

entry_points = \
{'console_scripts': ['aws-export-credentials = aws_export_credentials:main']}

setup_kwargs = {
    'name': 'aws-export-credentials',
    'version': '0.1.0',
    'description': 'Get AWS credentials from a profile to inject into other programs',
    'long_description': None,
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
