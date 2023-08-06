# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickrtape']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tickrtape',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Henry Trotter',
    'author_email': 'hbtrotter38@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
