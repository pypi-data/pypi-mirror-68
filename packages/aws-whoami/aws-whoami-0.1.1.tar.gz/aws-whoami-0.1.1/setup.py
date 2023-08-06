# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_whoami']
install_requires = \
['boto3']

entry_points = \
{'console_scripts': ['aws-whoami = aws_whoami:main']}

setup_kwargs = {
    'name': 'aws-whoami',
    'version': '0.1.1',
    'description': "A tool to show what AWS account and identity you're using",
    'long_description': None,
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
}


setup(**setup_kwargs)
