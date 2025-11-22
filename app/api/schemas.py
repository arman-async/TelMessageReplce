from pydantic import BaseModel

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
    name: str
    regex: str
    acction: enums.MessageActions
    message_replace: str
    entities: str
    inline_keyboard_json: str
    max_total_uses: int
    max_uses_per_user: int
    run_after_join_check: bool


class MessageActionsUpdate(MessageActionsCreate):
    pass
