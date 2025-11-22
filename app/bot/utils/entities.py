from pyrogram.types import MessageEntity
from pyrogram.enums import MessageEntityType


TYPE_MAP = {
    "mention": MessageEntityType.MENTION,
    "hashtag": MessageEntityType.HASHTAG,
    "cashtag": MessageEntityType.CASHTAG,
    "bot_command": MessageEntityType.BOT_COMMAND,
    "url": MessageEntityType.URL,
    "email": MessageEntityType.EMAIL,
    "phone_number": MessageEntityType.PHONE_NUMBER,
    "bold": MessageEntityType.BOLD,
    "italic": MessageEntityType.ITALIC,
    "underline": MessageEntityType.UNDERLINE,
    "strikethrough": MessageEntityType.STRIKETHROUGH,
    "spoiler": MessageEntityType.SPOILER,
    "code": MessageEntityType.CODE,
    "pre": MessageEntityType.PRE,
    "blockquote": MessageEntityType.BLOCKQUOTE,
    "text_link": MessageEntityType.TEXT_LINK,
    "text_mention": MessageEntityType.TEXT_MENTION,
    "bank_card": MessageEntityType.BANK_CARD,
    "custom_emoji": MessageEntityType.CUSTOM_EMOJI,
}


def dict_to_entitie(entity: dict) -> MessageEntity:
    entity_type = entity.get("type")

    if isinstance(entity_type, str):
        entity_type = TYPE_MAP.get(entity_type.lower(), MessageEntityType.UNKNOWN)

    return MessageEntity(
        type=entity_type,
        offset=entity.get("offset"),
        length=entity.get("length"),
        url=entity.get("url"),
        user=entity.get("user"),
        language=entity.get("language"),
        custom_emoji_id=entity.get("custom_emoji_id"),
    )


def list_to_entitie(entities: list[dict]) -> list[MessageEntity]:
    return [dict_to_entitie(entity) for entity in entities]
