# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numiner', 'numiner.classes']

package_data = \
{'': ['*']}

install_requires = \
['coveralls>=2.0.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'pandas>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['numiner = numiner.__main__:main',
                     'version = numiner.__main__:get_version']}

setup_kwargs = {
    'name': 'numiner',
    'version': '0.1.1',
    'description': 'NUM Miner (Tool to create open dataset for Handwritten Text Recognition)',
    'long_description': '<h1 align="center">\n  NUMiner\n</h1>\n\n<p align="center">\n  <a href="https://travis-ci.org/khasbilegt/numiner">\n    <img src="https://travis-ci.org/khasbilegt/numiner.svg?branch=master" alt="Build Status">\n  </a>\n  <a href="https://github.com/PyCQA/bandit">\n    <img src="https://img.shields.io/badge/security-bandit-yellow.svg"\n         alt="security: bandit">\n  </a>\n  <a href="https://badge.fury.io/py/numiner">\n    <img src="https://badge.fury.io/py/numiner.svg" alt="PyPI version" height="18">\n  </a>\n  <a href=\'https://coveralls.io/github/khasbilegt/numiner?branch=master\'>\n    <img src=\'https://coveralls.io/repos/github/khasbilegt/numiner/badge.svg?branch=master\' alt=\'Coverage Status\' />\n  </a>\n</p>\n\n<p align="center">\n  <a href="#installation">Installation</a> •\n  <a href="#how-to-use">How To Use</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#license">License</a>\n</p>\n\n<p align="center">This is a Python library that creates training images for Handwritten Text Recognition or HTR related researches</p>\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install numiner.\n\n```bash\npip install numiner\n```\n\n## How To Use\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Khasbilegt.TS',
    'author_email': 'khasbilegt.ts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khasbilegt/numiner/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
