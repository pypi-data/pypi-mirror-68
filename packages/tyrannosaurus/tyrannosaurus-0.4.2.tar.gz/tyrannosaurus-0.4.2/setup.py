# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyrannosaurus']

package_data = \
{'': ['*'], 'tyrannosaurus': ['resources/*']}

install_requires = \
['grayskull>=0.4,<0.5',
 'importlib-metadata>=1.6,<2.0',
 'requests>=2.23,<3.0',
 'tomlkit>=0.6.0,<0.7.0',
 'typer>=0.2,<0.3']

entry_points = \
{'console_scripts': ['tyrannosaurus = tyrannosaurus.cli:cli']}

setup_kwargs = {
    'name': 'tyrannosaurus',
    'version': '0.4.2',
    'description': 'Opinionated Python template and metadata synchronizer for 2020.',
    'long_description': '# Tyrannosaurus Reqs\n\n[![Docker](https://img.shields.io/docker/v/dmyersturnbull/tyrannosaurus)](https://hub.docker.com/repository/docker/dmyersturnbull/tyrannosaurus)\n[![Latest version on PyPi](https://badge.fury.io/py/tyrannosaurus.svg)](https://pypi.org/project/tyrannosaurus/)\n[![Documentation status](https://readthedocs.org/projects/tyrannosaurus/badge/?version=latest&style=flat-square)](https://tyrannosaurus.readthedocs.io/en/stable/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Build status](https://img.shields.io/pypi/status/tyrannosaurus)](https://pypi.org/project/tyrannosaurus/)\n[![Build & test](https://github.com/dmyersturnbull/tyrannosaurus/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/tyrannosaurus/actions)\n[![Travis](https://travis-ci.org/dmyersturnbull/tyrannosaurus.svg?branch=master)](https://travis-ci.org/dmyersturnbull/tyrannosaurus)\n\nAn opinionated Python template for 2020.\nNo setup.py, requirements.txt, or eggs.\n\nI wrote this after making nearly 50 commits to configure\nreadthedocs, PyPi, Tox, Docker, Travis, and Github actions.\nThis avoids that struggle for 99% of projects.\nJust clone and modify or use `tyrannosaurus new`.\nInstall with `pip install tyrannosaurus`.\n\n- _When you commit_, your code will be linted.\n- _When you push or make a pull request_, your code will be built and tested.\n  Metadata will be synced, security checks will be run, style will be checked,\n  documentation will be generated, and docker images, sdists, and wheels will be built.\n- _When you release on Github_, your code will be published on PyPi.\n  Just add `PYPI_TOKEN` as a Github repo secret.\n\n⚠ Status: Alpha. Generally works pretty well, but\n   the `sync` command does less than advertised.\n\n##### Other integrations:\n\nAlso comes with nice Github labels, a changelog template,\nConda recipe generation, and various other integrations.\nTyrannosaurus itself is included as a dependency to copy metadata between config files,\nsuch as the project version, description, copyright, and build and doc requirements.\n\n##### To run:\n\nTo run locally, install [Poetry](https://github.com/python-poetry/poetry)\nand [Tox](https://tox.readthedocs.io/en/latest/) (`pip install tox`).\nThen just type `tox` to build artifacts and run tests.\nSync metadata using `tyrannosaurus sync`.\nGenerate a Conda recipe with `tyrannosaurus recipe`,\nand an Anaconda environment file with `tyrannosaurus env`.\n\n[See the docs](https://tyrannosaurus.readthedocs.io/en/stable/) for more information.\n\n\n### Building, extending, and contributing\n\n[New issues](https://github.com/dmyersturnbull/tyrannosaurus/issues) and pull requests are welcome.\nTyrannosaurus is licensed under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n\n\n\n```text\n                                              .++++++++++++.\n                                           .++HHHHHHH^^HHH+.\n                                          .HHHHHHHHHH++-+-++.\n                                         .HHHHHHHHHHH:t~~~~~\n                                        .+HHHHHHHHHHjjjjjjjj.\n                                       .+NNNNNNNNN/++/:--..\n                              ........+NNNNNNNNNN.\n                          .++++BBBBBBBBBBBBBBB.\n .tttttttt:..           .++BBBBBBBBBBBBBBBBBBB.\n+tt+.      ``         .+BBBBBBBBBBBBBBBBBBBBB+++cccc.\nttt.               .-++BBBBBBBBBBBBBBBBBBBBBB++.ccc.\n+ttt++++:::::++++++BBBBBBBBBBBBBBBBBBBBBBB+..++.\n.+TTTTTTTTTTTTTBBBBBBBBBBBBBBBBBBBBBBBBB+.    .ccc.\n  .++TTTTTTTTTTBBBBBBBBBBBBBBBBBBBBBBBB+.      .cc.\n    ..:++++++++++++++++++BBBBBB++++BBBB.\n           .......      -LLLLL+. -LLLLL.\n                        -LLLL+.   -LLLL+.\n                        +LLL+       +LLL+\n                        +LL+         +ff+\n                        +ff++         +++:\n                        ++++:\n```\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/tyrannosaurus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
