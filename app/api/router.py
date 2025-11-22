from fastcrud import crud_router

from app import db

from . import schemas

forced_subscription = crud_router(
    session=db.get_session_depen,
    model=db.models.ForcedSubscription,
    create_schema=schemas.ForcedSubscriptionCreate,
    update_schema=schemas.ForcedSubscriptionUpdate,
    path="/forced_subscriptions",
    tags=["ForcedSubscriptions"],
)

message_action = crud_router(
    session=db.get_session_depen,
    model=db.models.MessageAction,
    create_schema=schemas.MessageActionsCreate,
    update_schema=schemas.MessageActionsUpdate,
    path="/message_actions",
    tags=["MessageActions"],
)
