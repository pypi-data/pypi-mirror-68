# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['micropython_wifi_setup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'micropython-wifi-setup',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'George Hawkins',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
