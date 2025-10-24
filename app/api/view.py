from sqladmin import ModelView, BaseView, expose
from app.db import models
from fastapi import Request

class CategoryForcedSubscription():
    NAME = "Forced Subscriptions"
    ICON = "fa fa-address-card"

class CategoryAction():
    NAME = "Action"
    ICON = "fa fa-bolt"

# ======= ForcedSubscriptions =======
class ForcedSubscription(ModelView, model=models.ForcedSubscription):
    name = "Channel"
    name_plural = "Channels"
    icon = "fa fa-plug"
    category = CategoryForcedSubscription().NAME
    category_icon = CategoryForcedSubscription().ICON

    # ========== Column Config ==========
    column_list = [
        models.ForcedSubscription.id,
        models.ForcedSubscription.name,
        models.ForcedSubscription.channel_id,
    ]
    column_searchable_list = [
        models.ForcedSubscription.id,
        models.ForcedSubscription.name,
        models.ForcedSubscription.invite_link,
        models.ForcedSubscription.channel_id,
        
    ]
    column_labels = {
        models.ForcedSubscription.id: "Id",
        models.ForcedSubscription.name: "Name",
        models.ForcedSubscription.channel_id: "Channel ID",
    }


    # ========== Form Config ==========
    form_columns = [
        models.ForcedSubscription.name,
        models.ForcedSubscription.channel_id,
        models.ForcedSubscription.invite_link,
    ]
    
    # ========== Permissions ==========
    def is_visible(self, request):
        return True

    def is_accessible(self, request):
        return True 




# ======= MessageActions =======
class MessageAction(ModelView, model=models.MessageAction):
    name = "Message Action"
    name_plural = "Message Actions"
    icon = "fa fa-comment"
    category = CategoryAction().NAME
    category_icon = CategoryAction().ICON

    # ========== Column Config ==========
    column_list = [
        models.MessageAction.id,
        models.MessageAction.regex,
        models.MessageAction.name,
        models.MessageAction.acction,
    ]
    column_searchable_list = [
        models.MessageAction.id,
        models.MessageAction.name,
        models.MessageAction.regex,
    ]
    column_labels = {
        models.MessageAction.id: "Id",
        models.MessageAction.name: "Name",
        models.MessageAction.regex: "Regex Select",
        models.MessageAction.acction: "Acction",
    }


    # ========== Form Config ==========
    form_columns = [
        models.MessageAction.name,
        models.MessageAction.regex,
        models.MessageAction.acction,
        models.MessageAction.message_replace,
    ]
    
    # ========== Permissions ==========
    def is_visible(self, request):
        return True

    def is_accessible(self, request):
        return True