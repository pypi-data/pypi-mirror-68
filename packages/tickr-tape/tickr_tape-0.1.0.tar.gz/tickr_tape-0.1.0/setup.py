# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickr_tape']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tickr-tape',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Henry Trotter',
    'author_email': 'hbtrotter38@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
