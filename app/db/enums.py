from enum import Enum


class MessageActions(Enum):
    IGNORE = "ignore"
    DELETE = "delete"
    REPLACE = "replace"
    ADS = "ads"
    EDIT = "EDIT"