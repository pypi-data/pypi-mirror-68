from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from quiz_bots import settings
from quiz_bots.bots_helpers import send_message_to_tg_chat
from quiz_bots.quiz_helpers import get_clean_text_of_answer
from quiz_bots.redis_utils import (
    connect_to_redis,
    get_answer_to_last_question_of_user,
    get_last_asked_question_from_redis,
    get_quiz_content_from_redis,
    get_random_question,
    save_last_asked_question_to_redis,
)

BUTTON_NEW_QUESTION = 'Новый вопрос'
BUTTON_SURRENDER = 'Сдаться'
BUTTON_SCORE = 'Мой счет'
QUESTION_IS_SET_INCORRECTLY_BUTTON = 'Вопрос составлен неверно'

redis_connection = connect_to_redis()
quiz_content = get_quiz_content_from_redis(redis_connection)

CHOOSING, WAIT_ANSWER = range(2)


def welcome_message(update, context):
    """Sends a welcome message to the chat when the bot starts."""
    first_name = update.message.from_user.first_name
    message_text = f'Приветствую, {first_name}! Для старта нажмите кнопку "Новый вопрос"'
    custom_keyboard = [[BUTTON_NEW_QUESTION]]
    send_message_to_tg_chat(
        update,
        message_text,
        custom_keyboard,
    )

    return CHOOSING


def handle_new_question_request(update, context) -> int:
    """Sends a random question to the user."""
    question, number_of_question = get_random_question(quiz_content)

    if context.user_data.get('was_the_surrender_button_pressed'):
        custom_keyboard = [
            [BUTTON_SURRENDER, BUTTON_SCORE],
            [QUESTION_IS_SET_INCORRECTLY_BUTTON],
        ]
    else:
        custom_keyboard = [
            [BUTTON_SURRENDER, BUTTON_SCORE],
        ]
    send_message_to_tg_chat(
        update,
        question['question'].replace('\n', ' '),
        custom_keyboard,
    )

    save_last_asked_question_to_redis(
        user_id=update.message.from_user.id,
        redis_connection=redis_connection,
        social_network='tg',
        number_of_question=number_of_question,
    )

    return WAIT_ANSWER


def handle_solution_attempt(update, context):
    """Checks answer of user."""
    last_asked_question = get_last_asked_question_from_redis(
        user_id=update.message.from_user.id,
        redis_connection=redis_connection,
        social_network='tg',
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_connection=redis_connection,
        last_asked_question=last_asked_question,
    )
    clean_answer = get_clean_text_of_answer(answer_to_last_question_of_user)
    if update.message.text.lower() == clean_answer:
        message_text = 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
        custom_keyboard = [[BUTTON_NEW_QUESTION]]
    else:
        message_text = 'Неправильно... Попробуешь ещё раз?'
        custom_keyboard = [[BUTTON_SURRENDER, BUTTON_SCORE]]

    send_message_to_tg_chat(
        update,
        message_text,
        custom_keyboard,
    )

    return CHOOSING


def handle_opportunity_to_surrender(update, context):
    """Handles clicking the "Surrender" button.

    The bot sends the user an answer to the question
    and sends the next question with the next message.
    """
    last_asked_question = get_last_asked_question_from_redis(
        user_id=update.message.from_user.id,
        redis_connection=redis_connection,
        social_network='tg',
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_connection=redis_connection,
        last_asked_question=last_asked_question,
    )
    send_message_to_tg_chat(
        update,
        answer_to_last_question_of_user,
    )
    context.user_data['was_the_surrender_button_pressed'] = True

    handle_new_question_request(update, context)

    return WAIT_ANSWER


def handler_question_is_incorrect(update, context):  # noqa: WPS226
    """Handles clicking the button 'The question is incorrect'."""
    custom_keyboard = [[BUTTON_SURRENDER, BUTTON_SCORE]]
    send_message_to_tg_chat(
        update,
        'Спасибо за фидбек! Ждем ответ на предыдущий вопрос!',
        custom_keyboard,
    )
    return WAIT_ANSWER


def cancel(update, context):
    """Sends a message to the chat when the bot finish work."""
    first_name = update.message.from_user.first_name
    message_text = f'Спасибо за участие в викторине, {first_name}!'
    custom_keyboard = [[BUTTON_NEW_QUESTION]]
    send_message_to_tg_chat(
        update,
        message_text,
        custom_keyboard,
    )


def start_tg_bot():
    """Launch the TG bot."""
    updater = Updater(settings.TG_TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', welcome_message)],

        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^Новый вопрос$'),
                    handle_new_question_request,
                ),
                MessageHandler(
                    Filters.regex('^Сдаться$'),
                    handle_opportunity_to_surrender,
                ),
            ],
            WAIT_ANSWER: [
                MessageHandler(
                    Filters.regex('^Сдаться$'),
                    handle_opportunity_to_surrender,
                ),
                MessageHandler(
                    Filters.regex('^Вопрос составлен неверно$'),
                    handler_question_is_incorrect,
                ),
                MessageHandler(
                    Filters.text,
                    handle_solution_attempt,
                ),
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
