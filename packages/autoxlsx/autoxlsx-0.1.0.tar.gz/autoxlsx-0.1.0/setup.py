# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoxlsx']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'openpyxl>=3.0.3,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['autoxlsx = autoxlsx.cli:cli']}

setup_kwargs = {
    'name': 'autoxlsx',
    'version': '0.1.0',
    'description': '',
    'long_description': '# README\n\n## Architecture\n\n[Diagramm](https://drive.google.com/file/d/1nRkJj-1Z-pQCY3Z-3_RDi36bKWVh-Q9p/view?usp=sharing)',
    'author': 'KhalidCK',
    'author_email': 'khalidCK@win.local',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
