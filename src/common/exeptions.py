class CommonException(Exception):
    pass


class UserNotAuthenticated(CommonException):
    pass


class IncorrectToken(CommonException):
    pass
