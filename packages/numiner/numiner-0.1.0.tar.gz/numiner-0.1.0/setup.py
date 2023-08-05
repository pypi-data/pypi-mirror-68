# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numiner', 'numiner.classes']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'pandas>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['numiner = numiner.__main__:main']}

setup_kwargs = {
    'name': 'numiner',
    'version': '0.1.0',
    'description': 'NUM Miner (Tool to create open dataset for Handwritten Text Recognition)',
    'long_description': '# NUMiner\n\nNUMiner is a Python library for creating training image for Handwritten Text Recognition or HTR. It uses prebuilt\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install numiner.\n\n```bash\npip install numiner\n```\n\n## Usage\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
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
