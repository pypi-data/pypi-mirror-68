# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['good_smell', 'good_smell.smells']

package_data = \
{'': ['*']}

install_requires = \
['astor', 'fire', 'flake8>=3,<4']

setup_kwargs = {
    'name': 'good-smell',
    'version': '0.16',
    'description': 'A linter/refactoring tool to make your code smell better!',
    'long_description': '# Good Smell - it makes your code smell good! \nA linting/refactoring library for python best practices and lesser-known tricks  \n---\n![Build](https://github.com/tadaboody/good_smell/workflows/Python%20package/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![PyPi version](https://pypip.in/v/good_smell/badge.png)](https://pypi.org/project/good-smell/)\n\n---\n\nThis Tool tries to find bits of code that are possible to make more pythonic, more beautiful by using the language features and standard library functions you might not know about\n\nFor example\nDirectly nested for loops (nested-for)\n```py\nfor i in seq_a:\n    for j in seq_b:\n        print(i, j)\n```\nwill be flattened to a nested comprehension\n```py\nimport itertools\nfor i, j in ((i,j) for i in seq_a for j in seq_b):\n    print(i, j)\n```\nFor a full list - check the list of [implemented smells](docs/smell_list.md)\n## Installing:\n```sh\npip install good_smell \n```\n## Usage (Is likely to change when version 1.0 is released):\n\nTo issue warnings, good_smell installs itself as a [flake8](http://flake8.pycqa.org/en/latest/) plugin with error codes starting with SML.\n\nTo automatically fix the code use ``good_smell fix``:\n\n```sh\ngood_smell fix PATH >PATH\ngood_smell fix PATH [--starting-line STARTING_LINE] [--end-line END_LINE]\n```\n\n## Developing\nSee [contributing guide](CONTRIBUTING)\n',
    'author': 'Tomer Keren',
    'author_email': 'tomer.keren.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tadaboody/good_smell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
