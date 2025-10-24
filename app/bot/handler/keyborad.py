from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.db.models import ForcedSubscription


def forced_join(
    channels: list[ForcedSubscription],
    text_button_check: str,
    url_button_check: str | None = None,
) -> InlineKeyboardMarkup:
    """
    Creates a join message with inline buttons for channels.

    :param channels: List of ForcedSubscription objects (each with name and invite_link)
    :return: Tuple of (message_text, InlineKeyboardMarkup)
    """
    buttons = []

    for ch in channels:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=ch.name,
                    url=ch.invite_link,
                ),
            ]
        )

    buttons.append(
        [
            (
                InlineKeyboardButton(text=text_button_check, callback_data="check_join")
                if url_button_check is None
                else InlineKeyboardButton(
                    text=text_button_check,
                    url=url_button_check,
                )
            ),
        ]
    )
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
