# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betterls']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['bls = betterls.ls:bls']}

setup_kwargs = {
    'name': 'betterls',
    'version': '1.2.0',
    'description': 'Better ls command.',
    'long_description': None,
    'author': 'Cyrus Yip',
    'author_email': 'cyruscmyip1@gmail.com',
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
