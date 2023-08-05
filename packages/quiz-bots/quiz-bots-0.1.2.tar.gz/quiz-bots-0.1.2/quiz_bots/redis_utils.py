import json
import secrets
from typing import Dict, Tuple

import redis

from quiz_bots import settings

REDIS_HOST, REDIS_PORT = settings.DB_ENDPOINT.split(':')
REDIS_PASSWORD = settings.DB_PASSWORD


def connect_to_redis() -> redis.client.Redis:
    """Creates a connection to the Redis database."""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )


def get_quiz_content_from_redis(redis_connection: redis.client.Redis):
    """Gets the content for the quiz from the database."""
    quiz_content = redis_connection.get('questions')
    if quiz_content:
        return json.loads(quiz_content)


def get_random_question(
    quiz_content: Dict[str, Dict[str, str]],
) -> Tuple[Dict[str, str], int]:
    """Gets a random question from the quiz content."""
    number_of_question = secrets.randbelow(len(quiz_content) + 1)
    return quiz_content[f'question_{number_of_question}'], number_of_question


def save_last_asked_question_to_redis(
    user_id, redis_connection, social_network: str, number_of_question: int,
) -> None:
    """Saves the user's question number in the database."""
    user = {
        f'user_{social_network}_{user_id}': {
            'last_asked_question': f'question_{number_of_question}',
        },
    }
    redis_connection.set('users', json.dumps(user))


def get_last_asked_question_from_redis(
    user_id, redis_connection, social_network: str,
):
    """Gets the last asked question from redis."""
    users_data = json.loads(redis_connection.get('users'))
    user_data = users_data[f'user_{social_network}_{user_id}']
    return user_data['last_asked_question']


def get_answer_to_last_question_of_user(
    redis_connection, last_asked_question: Dict[str, str],
) -> str:
    """Gets the text of the answer to the last question asked by the user."""
    quiz_content = json.loads(redis_connection.get('questions'))
    return quiz_content[last_asked_question]['answer']
