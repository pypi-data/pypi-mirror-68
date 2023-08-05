# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quiz_bots']

package_data = \
{'': ['*']}

install_requires = \
['environs>=7.4.0,<8.0.0',
 'python-telegram-bot>=12.7,<13.0',
 'redis>=3.5.1,<4.0.0',
 'vk-api>=11.8.0,<12.0.0']

entry_points = \
{'console_scripts': ['quiz-bots = quiz_bots.app:main']}

setup_kwargs = {
    'name': 'quiz-bots',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Bots for quiz\n\n<p align="center">\n  <a href="https://link_to_docs">\n    <img width="400"\n         src="https://sales-generator.ru/upload/resize_cache/iblock/bf9/790_395_2/bf9b6fa5187139c2dfc9819ec3115848.jpg"\n         alt="Bots for quiz" />\n  </a>\n</p>\n\n[![Build Status](https://travis-ci.com/velivir/quiz-bots.svg?branch=master)](https://travis-ci.com/velivir/quiz-bots)\n[![Maintainability](https://api.codeclimate.com/v1/badges/7bfc3ff61843cbf93a51/maintainability)](https://codeclimate.com/github/velivir/quiz-bots/maintainability)\n![GitHub](https://img.shields.io/github/license/velivir/quiz-bots)\n![Platform](https://img.shields.io/badge/platform-linux-brightgreen)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\n## How to install\n\n1. Create a bot in Telegram @via BotFather, and get it API token.\n2. Create redis account in [Redislabs](https://redislabs.com/), and after that create [cloud database](https://docs.redislabs.com/latest/rc/quick-setup-redis-cloud/) (you can choose free plan).\nGet your endpoint database url and port.\n3. Create VK\'s group, allow it send messages, and get access token for it.\n5. Put all necessary parameters to .env file.\n\n```\nTG_TOKEN=telegram_token\nDB_ENDPOINT=redis endpoint\nDB_PASSWORD=redis_password\nVK_GROUP_TOKEN=token_vkontakte\nVK_GROUP_ID=\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](https://github.com/vitaliy-antonov/quiz-bots/blob/master/LICENSE) file for details\n\n\n## Project Goals\n\nThe code is written for educational purposes on online-course for\nweb-developers [dvmn.org](https://dvmn.org/).\n',
    'author': 'Vitaliy Antonov',
    'author_email': 'vitaliyantonoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/velivir/quiz-bots',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
