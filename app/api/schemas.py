import json

from pydantic import BaseModel, field_validator

from app.db import enums


class ForcedSubscriptionCreate(BaseModel):
    name: str
    channel_id: int
    invite_link: str


class ForcedSubscriptionUpdate(ForcedSubscriptionCreate):
    pass


class ForcedSubscriptionRead(ForcedSubscriptionCreate):
    id: int

    class Config:
        from_attributes = True


class MessageActionsCreate(BaseModel):
    class Entities(BaseModel):
        type: str
        offset: int
        length: int
        url: str | None = None
        language:str | None = None
        custom_emoji_id:int| None = None

    class InlineKeyboardJson(BaseModel):
        class InlineKeyboard(BaseModel):
            text: str
            url: str

        inline_keyboard: list[list[InlineKeyboard]]

    name: str
    regex: str
    action: enums.MessageActions
    message_replace: str
    entities: list[Entities|None] = []
    inline_keyboard_json: InlineKeyboardJson | None
    max_total_uses: int
    max_uses_per_user: int
    run_after_join_check: bool

    @field_validator("entities", "inline_keyboard_json")
    def convert_dict_to_json(cls, v):
        if not v:
            return None
        
        if isinstance(v, BaseModel):
            v = v.model_dump()

        if isinstance(v, list):
            v = [
                item.model_dump() if isinstance(item, BaseModel) else item for item in v
            ]
        return json.dumps(v)


class MessageActionsUpdate(MessageActionsCreate):
    pass
