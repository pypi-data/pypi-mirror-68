# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sagasu']

package_data = \
{'': ['*']}

install_requires = \
['tweepy>=3.8.0,<4.0.0']

entry_points = \
{'console_scripts': ['sagasu = sagasu.app:app']}

setup_kwargs = {
    'name': 'sagasu',
    'version': '0.2.1',
    'description': 'sagasu is search all my contents',
    'long_description': None,
    'author': 'funwarioisii',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
