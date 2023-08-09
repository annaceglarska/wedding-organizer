from enum import Enum

def forDjango(cls):
    cls.do_not_call_in_templates = True
    return cls


@forDjango
class ErrorsEnum(Enum):
    SEATING_EXIST = 1
    GUEST_ERROR = 2


@forDjango
class StatusEnum(Enum):
    BEFORE_ADD = 1
    OK = 2
    ERROR = 3