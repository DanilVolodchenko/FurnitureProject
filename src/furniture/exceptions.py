class FurnitureProductException(Exception):
    pass


class IncorrectFile(FurnitureProductException):
    pass


class FurnitureProductNotFound(FurnitureProductException):
    pass
