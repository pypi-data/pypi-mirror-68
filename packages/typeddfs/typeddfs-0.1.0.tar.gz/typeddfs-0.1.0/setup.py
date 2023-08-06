# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typeddfs']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.6,<2.0',
 'natsort>=7.0,<8.0',
 'numpy>=1.18,<2.0',
 'pandas>=1.0,<2.0',
 'tomlkit>=0.6.0,<0.7.0',
 'typer>=0.2,<0.3']

setup_kwargs = {
    'name': 'typeddfs',
    'version': '0.1.0',
    'description': 'Pandas DataFrame subclasses that enforce structure and can self-organize.',
    'long_description': "# Typed DataFrames\n\n[![Build status](https://img.shields.io/pypi/status/typed-dfs)](https://pypi.org/project/typed-dfs/)\n[![Latest version on PyPi](https://badge.fury.io/py/typed-dfs.svg)](https://pypi.org/project/typed-dfs/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/typed-dfs.svg)](https://pypi.org/project/typed-dfs/)\n[![Documentation status](https://readthedocs.org/projects/typed-dfs/badge/?version=latest&style=flat-square)](https://readthedocs.org/projects/typed-dfs)\n[![Build & test](https://github.com/kokellab/typed-dfs/workflows/Build%20&%20test/badge.svg)](https://github.com/kokellab/typed-dfs/actions)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\nPandas DataFrame subclasses that enforce structure and can self-organize.\nBecause your functions can’t exactly accept _any_  DataFrame.\n[See the docs](https://typed-dfs.readthedocs.io/en/stable/) for more information.\n\nSimple example for a CSV like this:\n\n| key   | value  | note |\n| ----- | ------ | ---- |\n| abc   | 123    | ?    |\n\n\n```python\nfrom typing import Sequence\nfrom typeddfs import SimpleFrame, OrganizingFrame\n\nclass KeyValue(OrganizingFrame):\n\n    @classmethod\n    def required_index_names(cls) -> Sequence[str]:\n        return ['key']\n\n    @classmethod\n    def required_columns(cls) -> Sequence[str]:\n        return ['value']\n\n    @classmethod\n    def reserved_columns(cls) -> Sequence[str]:\n        return ['note']\n\n# will self-organizing and use 'key' as the index\ndf = KeyValue.read_csv('example.csv')\nprint(df.index.names, list(df.columns))  # ['key'], ['value', 'note']\n```\n\n[New issues](https://github.com/kokellab/typed-dfs/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/kokellab/typed-dfs/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus): `tyrannosaurus new typed-dfs`.\n\n\n",
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'dmyersturnbull',
    'maintainer_email': None,
    'url': 'https://github.com/kokellab/typed-dfs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
