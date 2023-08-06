# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typenv']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.10.3,<0.14.0']

setup_kwargs = {
    'name': 'typenv',
    'version': '0.1.4',
    'description': 'Typed environment variable parsing for Python',
    'long_description': '[![Build Status](https://travis-ci.com/hukkinj1/typenv.svg?branch=master)](https://travis-ci.com/hukkinj1/typenv)\n[![codecov.io](https://codecov.io/gh/hukkinj1/typenv/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/typenv)\n[![PyPI version](https://badge.fury.io/py/typenv.svg)](https://badge.fury.io/py/typenv)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n# typenv\n\n<!--- Don\'t edit the version line below manually. Let bump2version do it for you. -->\n> Version 0.1.4\n\n> Typed environment variable parsing for Python\n\n## Background\nTypenv does environment variable parsing with an API almost identical to the excellent [environs](https://github.com/sloria/environs). There are a few reasons why typenv might be preferred:\n- Type annotated typecast functions: type checkers are able to understand types of parsed environment variables.\n- More flexible prefix manipulation of environment variable names.\n- Validation of environment variable names.\n- Optional automatic uppercasing of environment variable names.\n- Ability to generate a .env.example that shows expected types of environment variables.\n- Less dependencies. No [marshmallow](https://github.com/marshmallow-code/marshmallow) required.\n\n## Installing\nInstalling from PyPI repository (https://pypi.org/project/typenv):\n```bash\npip install typenv\n```\n\n## Usage\n\n### Basics\nSet environment variables:\n```bash\nexport NAME=\'Harry Potter\'\nexport AGE=14\nexport IS_WIZARD=true\nexport PATRONUM_SUCCESS_RATE=0.92\nexport BANK_BALANCE=134599.01\nexport LUCKY_NUMBERS=7,3,11\nexport EXTRA_DETAILS=\'{"friends": ["Hermione", "Ron"]}\'\n```\n\nParse the values in Python:\n```python\nfrom typenv import Env\n\nenv = Env()\n\nNAME = env.str("NAME")  # => "Harry Potter"\nAGE = env.int("AGE")  # => 14\nIS_WIZARD = env.bool("IS_WIZARD")  # => True\nPATRONUM_SUCCESS_RATE = env.float("PATRONUM_SUCCESS_RATE")  # => 0.92\nBANK_BALANCE = env.decimal("BANK_BALANCE")  # => decimal.Decimal("134599.01")\nLUCKY_NUMBERS = env.list("LUCKY_NUMBERS", subcast=int)  # => [7, 3, 11]\nEXTRA_DETAILS = env.json("EXTRA_DETAILS")  # => {"friends": ["Hermione", "Ron"]}\n\n# Optional settings must have a default value\nIS_DEATH_EATER = env.bool("IS_DEATH_EATER", default=False)  # => False\n```\n\n### Supported types\nThe types supported by typenv are:\n* `env.str`\n* `env.int`\n* `env.bool`\n* `env.float`\n* `env.decimal`\n* `env.json`\n* `env.list`\n    * Takes a subcast argument for casting list items to one of `str`, `int` , `bool`, `float` or `decimal.Decimal`\n\n### Default values\nNormally, if an environment variable is not found, typenv raises an exception. If a default value is provided, however, that will be returned instead of raising.\n```python\nfrom typenv import Env\n\nenv = Env()\n\nBOOL = env.bool("NON_EXISTING_NAME", default=False)  # => False\nLIST = env.list("NON_EXISTING_NAME", default=["a", "b"])  # => ["a", "b"]\nOPTIONAL_INT = env.int("NON_EXISTING_NAME", default=None)  # => None\n```\n\n### Name prefixes\nTODO: document here\n\n### Name character set\nTypenv validates environment variable names. By default, the set of allowed characters includes upper case ASCII letters, digits and the underscore (`_`).\n\nThe set of allowed characters can be configured:\n```python\nfrom typenv import Env\n\nenv = Env(allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")\n```\n\n### Name uppercasing\n```bash\nexport UPPER_CASE_NAME=true\n```\n```python\nfrom typenv import Env\n\n# Environment variable names in type cast methods will automatically be upper\n# cased when `upper=True` is set here.\nenv = Env(upper=True)\n\nNAME = env.bool("upper_casE_Name")\n```\n\n### Validation\n```bash\nexport NAME=\'Harry Potter\'\nexport AGE=14\n```\n```python\nfrom typenv import Env\n\nenv = Env()\n\n# A single validator function\nNAME = env.str("NAME", validate=lambda n: n.startswith("Harry"))\n\n# A validator function can signal error by raising an exception\ndef is_positive(num):\n    if num <= 0:\n        raise Exception("Number is not positive")\n\n# A validator function can alternatively return `False` to signal an error\ndef is_less_than_thousand(num):\n    if num >= 1000:\n        return False\n    return True\n\n# Multiple validator functions can be passed as an iterable of callables\nAGE = env.int("AGE", validate=(is_positive, is_less_than_thousand))\n```\n\n### Reading from a `.env` file\nTODO: document here\n\n### Dumping parsed values\nTODO: document here\n\n## Acknowledgments\nThe public API of this library is almost an exact copy of [environs](https://github.com/sloria/environs), which is based on [envparse](https://github.com/rconradharris/envparse) and [django-environ](https://github.com/joke2k/django-environ). Credit for the interface goes to the authors of those libraries.\n',
    'author': 'hukkinj1',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/typenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
