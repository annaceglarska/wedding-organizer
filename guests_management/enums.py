from enum import Enum


def forDjango(cls):
    cls.do_not_call_in_templates = True
    return cls


@forDjango
class ErrorsEnum(Enum):
    SEATING_ERROR = 1
    SEATING_EXIST = 2
    GUEST_ERROR = 3
    GUEST_EXIST = 4
    TABLE_EXIST = 5
    TABLE_ERROR = 6


@forDjango
class StatusEnum(Enum):
    BEFORE_ADD = 1
    OK = 2
    ERROR = 3