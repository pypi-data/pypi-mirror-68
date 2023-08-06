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
    'version': '1.0.3',
    'description': 'Datetime to fixed hash. Shortable for lower precision',
    'long_description': '![hashdate](https://github.com/sloev/hashdate/raw/master/assets/logo.png)\n\n# HashDate \n\n[![Latest Version](https://img.shields.io/pypi/v/hashdate.svg)](https://pypi.python.org/pypi/hashdate) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nTurns Python datetimes (or iso dates with `cli`) into hashes.\n\nThe hashes support shortening to reduce precision, so a prefix of a hash will be the same datetime rounded to the given hashlength.\n\n## Cli usage\n\nCheck out the demo:\n```bash\n$ hashdate demo\n``` \n\nIts full of colors:\n\n[![asciicast](https://asciinema.org/a/kKaOD68BJXa11WA1ghW7vjqii.svg)](https://asciinema.org/a/kKaOD68BJXa11WA1ghW7vjqii)\n\nTurn your iso date into a hash:\n\n```bash\n$ hashdate date2hash 2020-05-13T22:30:47.136450\nhash: UCABCBDCCDAEHBDGEFA\n```\n\nThen if you only take the first 11 chars you get a datetime with less precision:\n\n```bash\n$ hashdate hash2date UCABCBDCCDA\ndatetime: 2020-05-13T22:30:00\n```\n\nyou can also secify to use emojis for charset if you want to:\n\n```bash\n$ hashdate date2hash 2020-05-13T22:30:47.136450 -c emoji\nhash: 🌹🐲🌼🥕🐲🥕🌲🐲🐲🌲🌼🍇🐐🥕🌲🌴🍇🐂🌼\n```\n\nand back again:\n\n```bash\n$ hash2date 🌹🐲🌼🥕🐲🥕🌲🐲🐲🌲🌼🍇🐐🥕🌲🌴🍇🐂🌼 -c emoji\ndatetime: 2020-05-13T22:30:47.136450\n```\n\n## Module usage\n\n```python\nimport datetime\nfrom hashdate import datetime_to_hash, hash_to_datetime\n\nnow = datetime.datetime.now()\nhash = datetime_to_hash(now)\ndt = hash_to_datetime(hash)\nassert now == dt\n```\n\n### Advanced\n\nUse emojis:\n\n```python\nimport datetime\nfrom hashdate import datetime_to_hash, hash_to_datetime\n\nnow = datetime.datetime.now()\nhash = datetime_to_hash(now, charset=\'emoji\')\ndt = hash_to_datetime(hash, charset=\'emoji\')\nassert now == dt\n```\n\nRegister more charsets:\n\n```python\nimport datetime\nfrom hashdate import register_charset, datetime_to_hash, hash_to_datetime\n\ncharset = "🌼🥕🐲🌲🍇🐂🌴🐐🍉🌺🍊🐽🍆🦎🍟🌱🐫🐍🐃🍍🌹🍕☘🌿🥓🐪🌷🏵🔥🐷🌳🌶🥒🐊🐗🐏🌵🌻🌽🐢🍋🍈💮🎃🌊🥔🌰🍀🍃💧💐🍂🐮🌸🐄🍄🍁🍞🥜🐑🥀🌭🐸🐖"\n\nregister_charset(\'my_emojis\', charset)\n\nnow = datetime.datetime.now()\nhash = datetime_to_hash(now, charset=\'my_emojis\')\ndt = hash_to_datetime(hash, charset=\'my_emojis\')\nassert now == dt\n```\n\n\n## Structure of a hashdate\n\n```\ncentenial: [...19,20,21...]\n|    quarter start month: [0,3,6,9]\n|    |   day in tens: [0:3]\n|    |   |   hour in tens: [0:5]\n|    |   |   |   minute in tens: [0:5]\n|    |   |   |   |   second in tens: [0:5]\n|    |   |   |   |   |   microsecond digits:[0:999999]\n|    |   |   |   |   |   |\nU CA B C B D C B A F C E BCDAAB  \n  |    |   |   |   |   | \n  |    |   |   |   |   second: [0:9]\n  |    |   |   |   minute: [0:9]\n  |    |   |   hour: [0:9]\n  |    |   day: [0:9]\n  |    month in quarter: [0,1,2]\n  year: [0:99]\n\n```',
    'author': 'sloev',
    'author_email': 'johanned.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sloev/hashdate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
