# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osxdocker', 'osxdocker.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['osxdocker = osxdocker:main']}

setup_kwargs = {
    'name': 'osxdocker',
    'version': '0.1.2',
    'description': 'A CLI for working with docker on OSX',
    'long_description': "[![Build Status](https://github.com/ConorSheehan1/osxdocker/workflows/ci/badge.svg)](https://github.com/ConorSheehan1/osxdocker/actions/)\n[![Documentation Status](https://readthedocs.org/projects/osxdocker/badge/?version=latest)](https://osxdocker.readthedocs.io)\n[![PyPI](https://img.shields.io/pypi/v/osxdocker)](https://pypi.org/project/osxdocker/)\n[![PyPI - License](https://img.shields.io/pypi/l/osxdocker)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# osxdocker\nA CLI for working with docker on OSX :apple: :snake:\n\nCurrently it just handles docker logs, because I found it annoying starting up a screen session to get to the docker vm every time I wanted to clear logs. :man_shrugging:  \nSee: https://stackoverflow.com/questions/42527291/clear-logs-in-native-docker-on-mac\n\n## Install\n```bash\n# python3 only\npip3 install osxdocker\n```\n\n## Dependencies\nAssumes you have `docker` and `screen` installed. If you don't, you can easily install them through [brew](https://brew.sh/). e.g.\n```\nbrew cask install docker\nbrew install screen\n```\n\n## Usage\n```bash\n# clear logs\nosxdocker clear_log $some_container_name\n\n# list available commands and flags\nosxdocker\n```\n\n![clear_log_example](docs/source/images/clear_log_example.png)\n\nThis cli uses https://github.com/google/python-fire  \nCheck out the docs for more details on usage, setting up bash completion, etc.  \nAlso worth noting:\n1. Because the package uses fire, it can be imported like a normal python package. e.g.\n    ```python\n    from osxdocker.docker_logs import DockerLogs\n    DockerLogs().log_path('foo')\n    ```\n2. This cli doesn't support `--version` due to a quirk with fire.\n    ```bash\n    osxdocker version # works fine\n    osxdocker --version # won't work\n    ```\n\n#### Edge cases and gotchas\nContainer names are unique, but containers are filtered by regex, so you can still run into issues.  \ne.g. You have two containers, named foo and foo_too.  \n`osxdocker cat_log foo` will fail because it matches foo and foo_too.  \n`osxdocker cat_log ^foo$` will work because it matches foo exactly.\n\n![multiple_container_error](docs/source/images/multiple_container_error.png)\n\n#### Developer notes\nSee [docs/source/dev.md](docs/source/dev.md)\n",
    'author': 'Conor Sheehan',
    'author_email': 'conor.sheehan.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ConorSheehan1/osxdocker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
