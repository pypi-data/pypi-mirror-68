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
    'version': '0.1.3',
    'description': '',
    'long_description': "# Bots for quiz\n\n## Description\n[![Build Status](https://travis-ci.com/velivir/quiz-bots.svg?branch=master)](https://travis-ci.com/velivir/quiz-bots)\n[![Maintainability](https://api.codeclimate.com/v1/badges/7bfc3ff61843cbf93a51/maintainability)](https://codeclimate.com/github/velivir/quiz-bots/maintainability)\n![GitHub](https://img.shields.io/github/license/velivir/quiz-bots)\n![Platform](https://img.shields.io/badge/platform-linux-brightgreen)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nThis repository contains Vk and TG bots for the quiz. They get used to the questions and check the correctness of the answers to them.\n\nBot examples:\n* [Tg bot](http://t.me/quiztg_bot)\n* [Vk bot](https://vk.com/club183378823) - write to group messages 'Новый вопрос'\n\n## Table of content\n\n- [Installation](#installation)\n- [How to use](#how-to-use)\n- [License](#license)\n- [Project goal](#project-goal)\n\n## Installation\n* Install using [pip](https://pypi.org/project/quiz-bots/):\n    ```bash\n    pip install quiz-bots\n    ```\n* Create a bot in Telegram via [BotFather](https://t.me/BotFather), and get it API token.\n* Create redis account in [Redislabs](https://redislabs.com/), and after that create [cloud database](https://docs.redislabs.com/latest/rc/quick-setup-redis-cloud/) (you can choose free plan).\nGet your endpoint database url and port.\n* Create VK's group, allow it send messages, and get access token for it.\n* Register environment variables in the operating system:\n\n    ```bash\n    export TELEGRAM_TOKEN=telegram_token\n    export DB_ENDPOINT=redis endpoint\n    export DB_PASSWORD=redis_password\n    export VK_GROUP_TOKEN=token_vkontakte\n    ```\n\n* Put the question files in a folder(sample files are in the repository folder [quiz_files_example](https://github.com/velivir/quiz-bots/tree/master/quiz_files_example)) and export quiz content to Redis:\n\n    ```bash\n    quiz-bots --export_quiz_content_to_redis [path_to_questions_folder]\n    ```\n\n## How to use\nRun TG bot:\n```bash\nquiz-bots --start_bot tg\n```\nRun VK bot:\n```bash\nquiz-bots --start_bot vk\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](https://github.com/vitaliy-antonov/quiz-bots/blob/master/LICENSE) file for details\n\n## Project Goal\n\nThe code is written for educational purposes on online-course for\nweb-developers [dvmn.org](https://dvmn.org/).\n",
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
