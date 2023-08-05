from enum import Enum


class ResponseType(Enum):
    RESPONSE_INVALID = 0
    RESPONSE_SIMPLE_CONTACT = 1
    RESPONSE_REPORTING = 2
    RESPONSE_NONE = 3
    RESPONSE_MAX_ID = 4
