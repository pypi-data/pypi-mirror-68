# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['harman_demo']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.51,<2.0', 'pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'harman-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Harmandeep Singh Dubb',
    'author_email': 'harmand1999@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
