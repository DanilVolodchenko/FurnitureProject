class UserException(Exception):
    pass


class UserNotFound(UserException):
    pass


class UserAlreadyExists(UserException):
    pass


class PermissionDenied(UserException):
    pass


class IncorrectToken(UserException):
    pass
