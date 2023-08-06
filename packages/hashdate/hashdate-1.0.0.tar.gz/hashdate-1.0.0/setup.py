# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hashdate']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['hashdate = hashdate.cli:cli']}

setup_kwargs = {
    'name': 'hashdate',
    'version': '1.0.0',
    'description': 'datetime to fixed hash. Shortable for lower precision',
    'long_description': None,
    'author': 'sloev',
    'author_email': 'johanned.valbjorn@gmail.com',
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
