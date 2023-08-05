# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['human_id']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['humanid-gen = human_id.cli:main']}

setup_kwargs = {
    'name': 'human-id',
    'version': '0.1.0',
    'description': 'Human readable IDs, in Python',
    'long_description': None,
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
