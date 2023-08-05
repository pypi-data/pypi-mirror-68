import glob
import json
import re
from dataclasses import asdict, dataclass
from typing import Dict, Generator, List

from quiz_bots.redis_utils import connect_to_redis


@dataclass
class Question:
    """Contains the data for the quiz question."""

    question: str
    answer: str


def get_raw_quiz_content_from_file(path_to_file: str) -> str:
    """Retrieves raw content for the quiz from a file for further processing."""
    with open(path_to_file, 'r', encoding='KOI8-R') as file_object:
        return file_object.read()


def fetch_quiz_data_from_text_block(
    text_block: str, text_blocks: Generator[str, None, None],
) -> Question:
    """Fetches query data from a text block."""
    return Question(
        question=re.sub(r'Вопрос \d+:\n', '', text_block),
        answer=re.sub(r'Ответ:\n', '', next(text_blocks)),
    )


def prepare_quiz_content_from(raw_quiz_content: str) -> List[Question]:
    """Prepares the content for the quiz from the raw data."""
    text_blocks = (text_block for text_block in raw_quiz_content.split('\n\n'))
    return [
        fetch_quiz_data_from_text_block(text_block, text_blocks)
        for text_block in text_blocks
        if text_block.startswith('Вопрос')
    ]


def get_all_quiz_content(file_paths: List[str]) -> List[Question]:
    """Getting quiz content from all files in folder."""
    all_quiz_content = []
    for file_path in file_paths:
        raw_quiz_content = get_raw_quiz_content_from_file(file_path)
        quiz_content = prepare_quiz_content_from(raw_quiz_content)
        all_quiz_content.extend(quiz_content)
    return all_quiz_content


def prepare_data_for_sending_to_redis(
    all_quiz_content: List[Question],
) -> Dict[str, Dict[str, str]]:
    """Convert quiz content to dict for sending to Redis."""
    return {
        f'question_{question_count + 1}': asdict(question_data)
        for question_count, question_data in enumerate(all_quiz_content)
    }


def send_quiz_content_to_redis(quiz_folder_path):
    """Sends quiz content to Redis."""
    redis_db = connect_to_redis()
    file_paths = list(glob.glob(f'{quiz_folder_path}/**/*.txt', recursive=True))
    all_quiz_content = get_all_quiz_content(file_paths)
    quiz_content_dict = prepare_data_for_sending_to_redis(all_quiz_content)
    redis_db.set('questions', json.dumps(quiz_content_dict))
