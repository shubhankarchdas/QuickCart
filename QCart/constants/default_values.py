from enum import Enum


class ResponseMessageType(Enum):
    SUCCESS='success'
    ERROR='error'
    WARNING='warning'
    INFO='info'
    NONE='null'