# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monetdb_pystethoscope']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'funcy>=1.13,<2.0', 'pymonetdb>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['pystethoscope = '
                     'monetdb_pystethoscope.stethoscope:stethoscope']}

setup_kwargs = {
    'name': 'monetdb-pystethoscope',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Panagiotis Koutsourakis',
    'author_email': 'kutsurak@monetdbsolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
