# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickrtape']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tickrtape',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Henry Trotter',
    'author_email': 'hbtrotter38@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
