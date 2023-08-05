# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xtip']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['xtip = xtip:main']}

setup_kwargs = {
    'name': 'xtip',
    'version': '0.2.0',
    'description': 'Run commands on selected text quickly',
    'long_description': '# Xtip\n\nA semi-clone of tanin47\'s [tip](https://github.com/tanin47/tip) but for X11 (i.e. Linux).\n\nAlpha stage, anything may change at any time.\n\nCustomised in python (but it\'s very easy to run shell commands from python if\nyou prefer another language).\n\n\n## Installation and setup\n\n* Install the core dependencies: `zenity`, `dmenu`, `xclip`\n  * e.g. on Debian-based OS: `sudo apt install zenity xclip suckless-tools`\n* Install xtip from pypi, e.g. `pip3 install xtip`\n* Bind a hotkey to run the `xtip` command using your preferred method.\n  * I use [sxhkd](https://github.com/baskerville/sxhkd), but I think most\n  desktop environments have a hotkey binding system.\n* Optionally install dependencies for any individual commands that you want to use:\n  * GoogleTranslate requires the python googtrans library\n  * Emacsclient requires emacs (obviously)\n\n\n## Writing your own commands\n\n\nFor most customisation of commands you should probably just write your own\n(because it only takes a few lines of python). You can write new commands in\n`~/.config/xtip/custom_commands.py`.\n\nTo do so: write a new class derived from `Command` and decorate it with\n`@command`, for example:\n\n\n```\nfrom typing import Optional\nfrom subprocess import run\n\nfrom xtip.commands import Command, command\n\n\n@command\nclass Emacsclient(Command):\n    unique_name = "Open in emacsclient"\n\n    def run(self, text: str) -> Optional[str]:\n        # TODO(david): Figure out a way to get the absolute path... maybe by\n        # guessing from a few possible prefixes?\n        run(["emacsclient", "-c", "-n", text])\n\n        # Return text from here to output it to the screen and clipboard\n        return None\n\n    def accepts(self, text: str) -> bool:\n        # TODO: only accept things that look like valid paths?\n        Return True\n```\n\nTODO: Do we need both inheritence and a decorator? Probably not!\n\n\n## TODO\n\n* Write some tests\n* CI builds\n* Try to display useful outputs in dmenu completion (e.g. converted datetimes)\n* Something better than dmenu? Better mouse support, popup at cursor.\n* Figure out how to construct an absolute path from a relative one\n',
    'author': 'David Shepherd',
    'author_email': 'davidshepherd7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidshepherd7/xtip',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
