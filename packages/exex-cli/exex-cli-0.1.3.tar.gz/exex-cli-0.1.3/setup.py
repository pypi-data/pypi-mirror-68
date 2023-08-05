# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exex_cli']

package_data = \
{'': ['*']}

install_requires = \
['cleo==0.6.8', 'exex>=0.1.7,<0.2.0']

setup_kwargs = {
    'name': 'exex-cli',
    'version': '0.1.3',
    'description': 'Command-line interface for extracting data from Excel documents.',
    'long_description': '# exex-cli [![Build Status](https://travis-ci.org/vikpe/exex-cli.svg?branch=master)](https://travis-ci.org/vikpe/exex-cli) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n> Command-line interface for extracting data from Excel documents.\n\n## Installation\n```sh\npip install exex-cli\n```\n\n## Usage\n### Synopsis\n```bash\nexex FILENAME --sheet SHEET --range RANGE --format FORMAT \n```\n\nParameter | Type | Default | Description\n--- | --- | --- | ---\n`FILENAME` | (required) string | | Path to .xlsx file. \n`[SHEET]` | (optional) string or int | `0` (first sheet) | Name or index of sheet\n`[RANGE]` | (optional) range | `all` (all values) | Range to get values from\n`[FORMAT]` | (optional) string | `text` | `text`, `table`, `json`, `csv`\n\n**Type of ranges**\n\nType | Syntax | Example\n--- | --- | ---\nAll values | `all` | `all`\nCell by name | `[COLUMN_NAME][ROW_NUMBER]` | `A1`\nCell by index | `[COLUMN_INDEX],[ROW_INDEX]` | `1,1`\nCell range | `[FROM]:[TO]` |  `A1:A3`\nColumn | `[COLUMN_NAME]` | `A`\nColumn range | `[FROM]:[TO]` | `A:C`\nRow | `[ROW_NUMBER]` | `1`\nRow range | `[FROM]:[TO]` | `1:3`\n\n### Examples\n\n**Get all values**\n```bash\npython -m exex_cli sample.xlsx \n```\n\n**Get all values as JSON**\n```bash\npython -m exex_cli sample.xlsx --format json \n```\n\n## Development\n\n**Tests** (local Python version)\n```sh\npoetry run pytest\n```\n\n**Tests** (all Python versions defined in `tox.ini`)\n```sh\npoetry run tox\n```\n\n**Code formatting** (black)\n```sh\npoetry run black .\n```\n',
    'author': 'Viktor Persson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vikpe/exex-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
