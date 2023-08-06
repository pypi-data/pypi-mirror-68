# Bots for quiz

## Description
[![Build Status](https://travis-ci.com/velivir/quiz-bots.svg?branch=master)](https://travis-ci.com/velivir/quiz-bots)
[![Maintainability](https://api.codeclimate.com/v1/badges/7bfc3ff61843cbf93a51/maintainability)](https://codeclimate.com/github/velivir/quiz-bots/maintainability)
![GitHub](https://img.shields.io/github/license/velivir/quiz-bots)
![Platform](https://img.shields.io/badge/platform-linux-brightgreen)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

This repository contains Vk and TG bots for the quiz. They get used to the questions and check the correctness of the answers to them.

Bot examples:
* [Tg bot](http://t.me/quiztg_bot)
* [Vk bot](https://vk.com/club183378823) - write to group messages 'Новый вопрос'

## Table of content

- [Installation](#installation)
- [How to use](#how-to-use)
- [License](#license)
- [Project goal](#project-goal)

## Installation
* Install using [pip](https://pypi.org/project/quiz-bots/):
    ```bash
    pip install quiz-bots
    ```
* Create a bot in Telegram via [BotFather](https://t.me/BotFather), and get it API token.
* Create redis account in [Redislabs](https://redislabs.com/), and after that create [cloud database](https://docs.redislabs.com/latest/rc/quick-setup-redis-cloud/) (you can choose free plan).
Get your endpoint database url and port.
* Create VK's group, allow it send messages, and get access token for it.
* Register environment variables in the operating system:

    ```bash
    export TELEGRAM_TOKEN=telegram_token
    export DB_ENDPOINT=redis endpoint
    export DB_PASSWORD=redis_password
    export VK_GROUP_TOKEN=token_vkontakte
    ```

* Put the question files in a folder(sample files are in the repository folder [quiz_files_example](https://github.com/velivir/quiz-bots/tree/master/quiz_files_example)) and export quiz content to Redis:

    ```bash
    quiz-bots --export_quiz_content_to_redis [path_to_questions_folder]
    ```

## How to use
Run TG bot:
```bash
quiz-bots --start_bot tg
```
Run VK bot:
```bash
quiz-bots --start_bot vk
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/vitaliy-antonov/quiz-bots/blob/master/LICENSE) file for details

## Project Goal

The code is written for educational purposes on online-course for
web-developers [dvmn.org](https://dvmn.org/).
