# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uvn_fira', 'uvn_fira.api', 'uvn_fira.core']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0', 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'uvn-fira',
    'version': '1.3.0',
    'description': 'The backend and API code for the Unscripted mini-game.',
    'long_description': '# Fira\n**Fira** is the main backend and API code for the minigame in [Unscripted](https://unscripted.marquiskurt.net), a visual novel about software development. Fira provides many facets of the minigame, including a public API that players can use to code solutions to the minigame puzzles, a configuration and data generator from level files, and a virtual machine that runs low-level code that the minigame processes (NadiaVM). Fira is named after Fira Sans, one of the game\'s characters.\n\n## Getting started\nFira comes pre-packaged in Unscripted but can be installed outside of the game to work better with IDEs and other Python tools such as Poetry.\n\n## Usage\nFor players installing this package to solve minigame puzzles, using the Fira package to access the API is relatively straightforward:\n\n```py\nfrom uvn_fira.api import get_level_information, CSPlayer, CSWorld\n\ngp, gw = get_level_information(0,\n                               fn_path=renpy.config.savedir + "/minigame",\n                               exists=renpy.loadable,\n                               load=renpy.exports.file)\n```\n\nDocumentation on the API is located inside of Unscripted by going to **Help &rsaquo; Minigame** or **Settings &rsaquo; Minigame**.\n\nThe documentation for the entire package is located at [https://fira.marquiskurt.net](https://fira.marquiskurt.net), which is useful for developers that wish to make custom toolkits that connect to the minigame\'s virtual machine or for modders that wish to make custom minigame levels.\n\n## Reporting bugs\nBugs and feature requests for Fira can be submitted on GitHub.\n\n## License\nThe Fira package is licensed under the Mozilla Public License v2.0.',
    'author': 'Marquis Kurt',
    'author_email': 'software@marquiskurt.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UnscriptedVN/fira',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
