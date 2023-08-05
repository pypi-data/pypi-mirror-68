# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betterls']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bls = betterls.ls:main']}

setup_kwargs = {
    'name': 'betterls',
    'version': '1.0.1',
    'description': 'Better ls command.',
    'long_description': None,
    'author': 'Cyrus Yip',
    'author_email': 'cyruscmyip1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
