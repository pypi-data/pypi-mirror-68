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
    'version': '0.1.0',
    'description': 'Run commands on selected text quickly',
    'long_description': "# Xtip\n\nA semi-clone of tanin47's [tip](https://github.com/tanin47/tip) but for X11 (i.e. Linux).\n\nAlpha stage, anything may change at any time.\n\nCustomised in python (but it's very easy to run shell commands from python if\nyou prefer another language).\n\n\n## Installation and setup\n\n* Install the core dependencies: `zenity`, `dmenu`, `xclip`\n  * e.g. on Debian-based OS: `sudo apt install zenity xclip suckless-tools`\n* Save x-tip.py into a directory on your `$PATH` and `chmod +x x-tip.py`\n* Bind a hotkey to it using your preferred method. \n  * I use [sxhkd](https://github.com/baskerville/sxhkd), but I think most\n  desktop environments have a hotkey binding system.\n* Optionally install dependencies for any individual commands that you want to use:\n  * GoogleTranslate requires the python googtrans library\n  * Emacsclient requires emacs (obviously)\n\n\n## Writing your own commands\n\n\nFor most customisation of commands you should probably just write your own\n(because it only takes a few lines of python).\n\nTo do so: write a new class derived from `Command` and decorate it with `@command`.\n\nTODO: better docs?\n\n\n## TODO\n\n* Write some tests\n* Set up typechecking properly\n* Add support for config files to specify commands\n* Add support for installing using `pip` (and break up into multiple files)\n* Try to display useful outputs in dmenu completion (e.g. converted datetimes)\n* Something better than dmenu? Better mouse support, popup at cursor.\n* Figure out how to construct an absolute path from \n",
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
