# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rchat']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'rocketchat-API>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['rchat = rchat.cli:cli']}

setup_kwargs = {
    'name': 'rchat',
    'version': '0.0.1',
    'description': 'A simple RocketChat command line client',
    'long_description': '# rchat\n![build](https://github.com/jvrsantacruz/rchat/workflows/Python%20package/badge.svg?branch=master) \n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\nA simple RocketChat command line client\n\n    rchat --to #team "Hello World!"\n\n## Command line\n\nrchat comes with a command line interface. See help for more information:\n\nSee `rchat --help`\n\n## Development\n\nFrom the root of the application directory, create a python environment,\ninstall the application in development mode along with its dependencies and\nrun it locally:\n\n    virtualenv env\n    . env/bin/activate\n    pip install --upgrade pip\n    pip install -e . -r requirements.txt -r dev-requirements.txt\n\nTests can be run using *tox* (recommended):\n\n    pip install tox\n    tox\n\nOr directly by calling *py.test*:\n\n    python -m pytest\n\n## TODO\n\n- Send private messages\n- Send message from files\n- Send message from stdin\n- Upload files\n- Upload images\n- Read messages\n- Listen to new messages\n- Autocomplete emojis\n- Autocomplete users\n- Autocomplete channels\n- Config file\n- Logging and debug\n- Debian Packaging\n- Bundled Packaging\n- Pypi version\n- Versioning script\n- Improve startup time\n- Define groups of users\n- Allow to get reactions\n- Allow for threads\n- Implement (pre|post) message hooks\n- Implement (pre|post) reaction hooks\n',
    'author': 'Javier Santacruz',
    'author_email': 'javier.santacruz.lc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jvrsantacruz/rchat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
