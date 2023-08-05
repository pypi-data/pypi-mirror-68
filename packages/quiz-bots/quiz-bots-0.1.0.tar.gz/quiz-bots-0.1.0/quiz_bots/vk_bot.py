from typing import List, Optional

import vk_api
from vk_api.keyboard import VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll

from quiz_bots import settings
from quiz_bots.bots_helpers import (
    Button,
    make_keyboard_of_vk,
    send_message_to_vk_chat,
)
from quiz_bots.quiz_helpers import get_clean_text_of_answer
from quiz_bots.redis_utils import (
    connect_to_redis,
    get_answer_to_last_question_of_user,
    get_last_asked_question_from_redis,
    get_quiz_content_from_redis,
    get_random_question,
    save_last_asked_question_to_redis,
)

redis_connection = connect_to_redis()
quiz_content = get_quiz_content_from_redis(redis_connection)
SOCIAL_NETWORK = 'vk'

BUTTON_NEW_QUESTION = Button(text='Новый вопрос', color=VkKeyboardColor.PRIMARY)
BUTTON_SURRENDER = Button(text='Сдаться', color=VkKeyboardColor.NEGATIVE)
BUTTON_SCORE = Button(text='Мой счет', color=VkKeyboardColor.POSITIVE)
QUESTION_IS_SET_INCORRECTLY_BUTTON = Button(text='Вопрос составлен неверно', color=VkKeyboardColor.DEFAULT)


def handle_new_question_request(vk, event, is_clicked_surrender_button: float) -> None:
    """Sends a random question to the user."""
    question, number_of_question = get_random_question(quiz_content)
    user_id = event.user_id

    if is_clicked_surrender_button:
        top_buttons = [BUTTON_SURRENDER, BUTTON_SCORE]
        bottom_buttons: Optional[List[Button]] = [QUESTION_IS_SET_INCORRECTLY_BUTTON]
    else:
        top_buttons = [BUTTON_SURRENDER, BUTTON_SCORE]
        bottom_buttons = None

    send_message_to_vk_chat(
        social_network_api=vk,
        user_id=user_id,
        keyboard=make_keyboard_of_vk(
            top_buttons=top_buttons,
            bottom_buttons=bottom_buttons,
        ),
        message=question['question'].replace('\n', ' '),
    )

    save_last_asked_question_to_redis(
        user_id=user_id,
        redis_connection=redis_connection,
        social_network=SOCIAL_NETWORK,
        number_of_question=number_of_question,
    )


def handle_solution_attempt(vk, event) -> None:
    """Checks answer of user."""
    user_id = event.user_id
    last_asked_question = get_last_asked_question_from_redis(
        user_id=user_id,
        redis_connection=redis_connection,
        social_network=SOCIAL_NETWORK,
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_connection=redis_connection,
        last_asked_question=last_asked_question,
    )
    if event.text.lower() == get_clean_text_of_answer(answer_to_last_question_of_user):
        top_buttons = [BUTTON_NEW_QUESTION]
        message = 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
    else:
        top_buttons = [BUTTON_SURRENDER, BUTTON_SCORE]
        message = 'Неправильно... Попробуешь ещё раз?'

    send_message_to_vk_chat(
        social_network_api=vk,
        user_id=user_id,
        keyboard=make_keyboard_of_vk(
            top_buttons=top_buttons,
            bottom_buttons=None,
        ),
        message=message,
    )


def handle_opportunity_to_surrender(vk, event) -> None:
    """Handles clicking the "Surrender" button.

    The bot sends the user an answer to the question
    and sends the next question with the next message.
    """
    user_id = event.user_id
    last_asked_question = get_last_asked_question_from_redis(
        user_id=user_id,
        redis_connection=redis_connection,
        social_network=SOCIAL_NETWORK,
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_connection=redis_connection,
        last_asked_question=last_asked_question,
    )
    send_message_to_vk_chat(
        social_network_api=vk,
        user_id=user_id,
        message=answer_to_last_question_of_user,
    )
    handle_new_question_request(vk, event, is_clicked_surrender_button=True)


def handler_question_is_incorrect(vk, event) -> None:
    """Handles clicking the button 'The question is incorrect'."""
    send_message_to_vk_chat(
        social_network_api=vk,
        user_id=event.user_id,
        keyboard=make_keyboard_of_vk(
            top_buttons=[BUTTON_SURRENDER, BUTTON_SCORE],
            bottom_buttons=None,
        ),
        message='Спасибо за фидбек! Ждем ответ на предыдущий вопрос!',
    )


def start_vk_bot():  # noqa: WPS210, WPS231
    """Launch the VK bot."""
    vk_group_token = settings.VK_GROUP_TOKEN
    vk_session = vk_api.VkApi(token=vk_group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                handle_new_question_request(vk, event, is_clicked_surrender_button=False)
            elif event.text == 'Сдаться':
                handle_opportunity_to_surrender(vk, event)
            elif event.text == 'Вопрос составлен неверно':
                handler_question_is_incorrect(vk, event)
            else:
                handle_solution_attempt(vk, event)
