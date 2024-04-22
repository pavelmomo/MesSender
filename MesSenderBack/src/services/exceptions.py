"""
Модуль содержит исключения, генерируемые слоем сервисов приложения

"""

class IncorrectData(Exception):
    pass


class UserNotExist(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidToken(Exception):
    pass


class TokenExpire(Exception):
    pass


class AccessDenied(Exception):
    pass
