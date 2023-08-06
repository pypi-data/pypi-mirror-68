# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rip']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'az-rip',
    'version': '0.0.1',
    'description': 'az-rip',
    'long_description': None,
    'author': 'Stefano Borini',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
