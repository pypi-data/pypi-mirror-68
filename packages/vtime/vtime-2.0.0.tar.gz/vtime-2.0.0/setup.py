# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vtime']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vtime',
    'version': '2.0.0',
    'description': 'Time related functions',
    'long_description': '# Palettes\n[![Build Status](https://travis-ci.com/villoro/v-time.svg?branch=master)](https://travis-ci.com/villoro/v-time)\n[![codecov](https://codecov.io/gh/villoro/v-time/branch/master/graph/badge.svg)](https://codecov.io/gh/villoro/v-time)\n\nTime related functions\n\n## Authors\n* [Arnau Villoro](https://villoro.com)\n\n## License\nThe content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).\n\n## Nomenclature\nBranches and commits use some prefixes to keep everything better organized.\n\n### Branches\n* **f/:** features\n* **r/:** releases\n* **h/:** hotfixs\n\n### Commits\n* **[NEW]** new features\n* **[FIX]** fixes\n* **[REF]** refactors\n* **[PYL]** [pylint](https://www.pylint.org/) improvements\n* **[TST]** tests\n',
    'author': 'Arnau Villoro',
    'author_email': 'arnau@villoro.com',
    'maintainer': 'Arnau Villoro',
    'maintainer_email': 'arnau@villoro.com',
    'url': 'https://github.com/villoro/vtime',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
