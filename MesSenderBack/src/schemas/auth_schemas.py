from enum import Enum


class TokenTransportTypes(str, Enum):
    cookie = 'cookie'
    header = 'header'
