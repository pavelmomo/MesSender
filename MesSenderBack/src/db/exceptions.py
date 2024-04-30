class DbError(Exception):
    pass

class DbConnectionError(DbError):
    pass

class IncorrectData(Exception):
    pass