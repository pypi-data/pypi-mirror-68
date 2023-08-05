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
    'version': '0.2.0',
    'description': '',
    'long_description': '# README\n\nWhen you need to carrefully fill-out an Excel file, it can be tricky.\n\nIt\'s even worse when the sheet is so ugly that it kind of burn your soul every time you open it.\n\nThis package try to tackle optimise that: writing plain yaml and never open the damn Excel file again.\n\n## Install\n\n```shell\npip install autoxlsx\n```\n\n## How to use\n\nA simple workbook\n\n**myugly.xlsx**\n\n![excelTable](img/eg_simple.png)\n\n`Name`,`function` & `age` are inputs others (E) are calculated by Excel formula.\n\n### Write model\n\nUsually people are picky about their excel format, so I expect this part to be quite static.\n\n**Model.yaml**\n\n```yaml\n- sheetname: mysheet\n  parameters:\n    #that\'s an employee first name\n    - parameter: "name"\n      position: "C4"\n    #here you have a function\n    #note: nobody care\n    - parameter: "function"\n      position: "C5"\n    #same nobody care but put something\n    - parameter: "age"\n      position: "C6"\n```\n### Write values\n\nThis part that will change often.\n\n**Values.yaml**\n\n```yaml\nmysheet.name: Bob\nmysheet.function: Sword man\nmysheet.age: 42\n```\n\nThe key use a dot notation to point to a specific value in the whole workbook. Note that parameter are defined in the `model.yaml`\n\n### Update excel\n\nUse the cli utility.\n\nIt will update inplace the excel file writing to the correct cells.\n\n```shell\nautoxlsx model.yaml values.yaml myugly.xlsx\n```\n\n## Example\n\nSee `tests/data/` for more example',
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
