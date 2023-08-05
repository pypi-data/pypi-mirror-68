# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwh_permissions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pwh-permissions',
    'version': '1.2.1',
    'description': 'A simple permissions parsing library for Python',
    'long_description': None,
    'author': 'Mark Hall',
    'author_email': 'mark.hall@work.room3b.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
