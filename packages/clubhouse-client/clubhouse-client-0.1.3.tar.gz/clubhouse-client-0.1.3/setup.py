# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clubhouse_client', 'clubhouse_client.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'clubhouse-client',
    'version': '0.1.3',
    'description': 'An unofficial python client for clubhouse.io',
    'long_description': None,
    'author': 'Michael J Burling',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mjburling/clubhouse-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
