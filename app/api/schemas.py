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


class MessageActionsUpdate(MessageActionsCreate):
    pass
