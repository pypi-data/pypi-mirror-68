# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cocinero', 'cocinero.plugins']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['cocinero = cocinero:cli']}

setup_kwargs = {
    'name': 'cocinero',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ricardo Gomes',
    'author_email': 'desk467@gmail.com',
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
