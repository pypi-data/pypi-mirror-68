from dataclasses import dataclass
from typing import List, Optional

import telegram
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


@dataclass
class Button:
    """Button of bot keyboard."""

    text: str
    color: VkKeyboardColor


def make_keyboard_of_vk(
    top_buttons: List[Button], bottom_buttons: Optional[List[Button]],
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
    social_network_api,
    user_id: int,
    message: str,
    keyboard: VkKeyboard = None,
) -> None:
    """Sends a message to the vk chat."""
    if keyboard:
        social_network_api.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard,
            message=message,
        )
    else:
        social_network_api.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            message=message,
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
