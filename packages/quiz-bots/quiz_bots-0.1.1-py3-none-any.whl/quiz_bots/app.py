import argparse

from quiz_bots.quiz import send_quiz_content_to_redis
from quiz_bots.tg_bot import start_tg_bot
from quiz_bots.vk_bot import start_vk_bot


def get_args() -> argparse.Namespace:
    """Getting arguments from command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start_bot',
        type=str,
        choices=['vk', 'tg'],
        help='Which bot to launch?',
    )

    parser.add_argument(
        '--quiz_questions_folder_path',
        type=str,
        help='Specify path to folder with quiz questions files',
    )
    return parser.parse_args()


def main() -> None:
    """Entry point."""
    args = get_args()
    start_bot = args.start_bot
    quiz_questions_folder_path = args.quiz_questions_folder_path

    if start_bot == 'tg':
        start_tg_bot()
    elif start_bot == 'vk':
        start_vk_bot()

    if quiz_questions_folder_path:
        send_quiz_content_to_redis(quiz_questions_folder_path)


if __name__ == '__main__':
    main()
