# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysenec']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

entry_points = \
{'console_scripts': ['senec = pysenec.cli:main']}

setup_kwargs = {
    'name': 'pysenec',
    'version': '0.1.0',
    'description': 'Unofficial, local SENEC Battery Client',
    'long_description': '# pySenec: Python Client for Senec Home\n\nTargeted at the Senec Home V2.1 System.\n\n\n\n## References\n\nI have used the [ioBroker.senec](https://github.com/nobl/ioBroker.senec) for the API details.\n',
    'author': 'Mikołaj Chwalisz',
    'author_email': 'm.chwalisz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mchwalisz/pysenec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
