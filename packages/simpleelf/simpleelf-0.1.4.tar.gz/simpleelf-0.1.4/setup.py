# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleelf']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10.54,<3.0.0', 'pytest>=4.6.10,<5.0.0']

setup_kwargs = {
    'name': 'simpleelf',
    'version': '0.1.4',
    'description': 'Simple ELF parser and builder',
    'long_description': None,
    'author': 'DoronZ',
    'author_email': 'doron88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doronz88/simpleelf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<4.0',
}


setup(**setup_kwargs)
