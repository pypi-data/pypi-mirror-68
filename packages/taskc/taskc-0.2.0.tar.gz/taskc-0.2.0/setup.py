# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskc']

package_data = \
{'': ['*'], 'taskc': ['fixture/*', 'fixture/pki/*']}

install_requires = \
['attrs', 'six']

setup_kwargs = {
    'name': 'taskc',
    'version': '0.2.0',
    'description': "A python client library for taskwarrior's taskd",
    'long_description': None,
    'author': 'Jack Laxson',
    'author_email': 'jackjrabbit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jrabbit/taskd-client-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
