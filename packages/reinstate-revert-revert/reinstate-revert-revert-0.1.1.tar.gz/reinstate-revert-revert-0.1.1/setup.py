# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reinstate_revert_revert']

package_data = \
{'': ['*']}

install_requires = \
['dulwich>=0.19.16,<0.20.0']

entry_points = \
{'console_scripts': ['reinstate-revert-revert = reinstate_revert_revert.cli:main']}

setup_kwargs = {
    'name': 'reinstate-revert-revert',
    'version': '0.1.1',
    'description': 'pre-commit plugin to improve default commit messages when reverting reverts',
    'long_description': '',
    'author': 'Erik Ogan',
    'author_email': 'erik@ogan.net',
    'maintainer': 'Erik Ogan',
    'maintainer_email': 'erik@ogan.net',
    'url': 'https://github.com/erikogan/reinstate-revert-revert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
