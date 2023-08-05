# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myprss']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'defusedxml>=0.6.0,<0.7.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'myprss',
    'version': '0.1.6',
    'description': 'rss reader for terminal',
    'long_description': None,
    'author': 'rarnal',
    'author_email': 'arnal.romain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
