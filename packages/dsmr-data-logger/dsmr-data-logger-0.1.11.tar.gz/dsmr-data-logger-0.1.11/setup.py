# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsmr', 'dsmr.dsmr', 'dsmr.plugins']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'configparser>=5.0.0,<6.0.0',
 'dsmr_parser>=0.18,<0.19',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['dsmr = dsmr.cli:main']}

setup_kwargs = {
    'name': 'dsmr-data-logger',
    'version': '0.1.11',
    'description': 'DSMR data logger',
    'long_description': '# p1-data-logger',
    'author': 'Pascal Prins',
    'author_email': 'pascal.prins@foobar-it.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paprins/dsmr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
