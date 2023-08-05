# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['turbot', 'turnips']

package_data = \
{'': ['*'], 'turbot': ['data/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'discord-py>=1.3.3,<2.0.0',
 'dunamai>=1.1.0,<2.0.0',
 'humanize>=2.4.0,<3.0.0',
 'hupper>=1.10.2,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['turbot = turbot:main']}

setup_kwargs = {
    'name': 'turbot',
    'version': '5.0.3',
    'description': 'Provides a Discord client and utilities for everything Animal Crossing: New Horizons.',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/theastropath/turbot/master/turbot.png" />\n\n# Turbot\n\n[![build][build-badge]][build]\n[![pypi][pypi-badge]][pypi]\n[![python][python-badge]][python]\n[![codecov][codecov-badge]][codecov]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n\nA Discord bot for everything _Animal Crossing: New Horizons_.\n\n![screenshot](https://user-images.githubusercontent.com/1903876/80841531-787c2f00-8bb4-11ea-8975-cc619b978635.png)\n\n## 🤖 Running the bot\n\nFirst install `turbot` using [`pip`](https://pip.pypa.io/en/stable/):\n\n```shell\npip install turbot\n```\n\nThen you must configure two things:\n\n1. Your Discord bot token.\n2. The list of channels you want `turbot` to monitor.\n\nTo provide your Discord bot token either set an environment variable named\n`TURBOT_TOKEN` to the token or paste it into a file named `token.txt`.\n\nFor the list of channels you can provide channel names on the command line using\nany number of `--channel "name"` options. Alternatively you can create a file\nnamed `channels.txt` where each line of the file is a channel name.\n\nMore usage help can be found by running `turbot --help`.\n\n## 📱 Using the bot\n\nOnce you\'ve connected the bot to your server, you can interact with it over\nDiscord via the following commands in any of the authorized channels.\n\n- `!about`: Get information about Turbot\n- `!help`: Provides detailed help about all of the following commands\n\n### 🤔 User Preferences\n\nThese commands allow users to set their preferences. These preferences are used\nto make other commands more relevant, for example by converting times to the\nuser\'s preferred timezone.\n\n- `!info`: Get a user\'s information\n- `!pref`: Set a user preference; use command to get a list of available options\n\n### 💸 Turnips\n\nThese commands help users buy low and sell high in the stalk market.\n\n- `!bestbuy`: Look for the best buy\n- `!bestsell`: Look for the best sell\n- `!buy`: Save a buy price\n- `!clear`: Clear your price data\n- `!graph`: Graph price data\n- `!history`: Get price history\n- `!lastweek`: Get graph for last week\'s price data\n- `!oops`: Undo the last price data\n- `!predict`: Predict your price data for the rest of the week\n- `!reset`: Reset all users\' data\n- `!sell`: Save a sell price\n\n### 🐟 Fish and Bugs\n\nProvides users with information on where and when to catch critters.\n\n- `!bugs`: Get information on bugs\n- `!fish`: Get information on fish\n- `!new`: Get information on newly available fish and bugs\n\n### 🦴 Fossils & 🖼️ Art\n\nWhen a community of users tracks collectables and trades them between each\nother, everyone finishes collecting everything in the game so much more quickly\nthan they would on their own.\n\nThese commands can also help users tell fake art from real art.\n\n- `!allfossils`: Get a list of all possible fossils\n- `!art`: Get information on an art piece\n- `!collect`: Collect fossils or art\n- `!collected`: Show collected fossils and art\n- `!count`: Count the number of collected fossils and art\n- `!neededfossils`: Get what fossils are needed by users\n- `!search`: Search for someone who needs a fossil or art\n- `!uncollect`: Remove a fossil or art from your collection\n- `!uncollected`: Get fossils and art not yet collected\n\n---\n\n[MIT][mit] © [TheAstropath][theastropath], [lexicalunit][lexicalunit] et [al][contributors]\n\n[black-badge]:      https://img.shields.io/badge/code%20style-black-000000.svg\n[black]:            https://github.com/psf/black\n[build-badge]:      https://github.com/theastropath/turbot/workflows/build/badge.svg\n[build]:            https://github.com/theastropath/turbot/actions\n[codecov-badge]:    https://codecov.io/gh/theastropath/turbot/branch/master/graph/badge.svg\n[codecov]:          https://codecov.io/gh/theastropath/turbot\n[contributors]:     https://github.com/theastropath/turbot/graphs/contributors\n[lexicalunit]:      http://github.com/lexicalunit\n[mit-badge]:        https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]:              https://opensource.org/licenses/MIT\n[python-badge]:     https://img.shields.io/badge/python-3.7+-blue.svg\n[python]:           https://www.python.org/\n[theastropath]:     https://github.com/theastropath\n[pypi]:             https://pypi.org/project/turbot/\n[pypi-badge]:       https://img.shields.io/pypi/v/turbot\n',
    'author': 'TheAstropath',
    'author_email': 'theastropath@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theastropath/turbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
