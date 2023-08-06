# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyarr']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'pyarr',
    'version': '0.9.0',
    'description': 'A Sonarr and Radarr API Wrapper',
    'long_description': None,
    'author': 'Steven Marks',
    'author_email': 'marksie1988@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/totaldebug/PyArr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
