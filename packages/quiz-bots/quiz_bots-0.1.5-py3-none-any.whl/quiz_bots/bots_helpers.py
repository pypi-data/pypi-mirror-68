from dataclasses import dataclass
from typing import List, Optional

import telegram
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


@dataclass
class BotKeyboardButton:
    """Button of bot keyboard."""

    text: str
    color: VkKeyboardColor


def make_keyboard_of_vk(
    top_buttons: List[BotKeyboardButton], bottom_buttons: Optional[List[BotKeyboardButton]],
) -> VkKeyboard:
    """Sends the keyboard to the Vk user."""
    keyboard = VkKeyboard(one_time=True)

    for top_button in top_buttons:
        keyboard.add_button(top_button.text, color=top_button.color)

    if not bottom_buttons:
        return keyboard.get_keyboard()

    keyboard.add_line()

    for bottom_button in bottom_buttons:
        keyboard.add_button(bottom_button.text, color=bottom_button.color)

    return keyboard.get_keyboard()


def send_message_to_vk_chat(
    vk_session,
    user_id: int,
    message_text: str,
    custom_keyboard: VkKeyboard = None,
) -> None:
    """Sends a message to the vk chat."""
    if custom_keyboard:
        vk_session.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=custom_keyboard,
            message=message_text,
        )
    else:
        vk_session.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            message=message_text,
        )


def send_message_to_tg_chat(
    update, message_text: str, custom_keyboard=None,
) -> None:
    """Sends a message to the tg chat."""
    if custom_keyboard:
        update.message.reply_text(
            message_text,
            reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard),
        )
    else:
        update.message.reply_text(message_text)
