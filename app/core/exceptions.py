class NotFoundError(Exception):
    def __init__(self, entity: str) -> None:
        self.entity = entity
        self.detail = f"{entity} not found"
        super().__init__(self.detail)


class DataIntegrityError(Exception):
    def __init__(self, message: str = "Data integrity violation") -> None:
        super().__init__(message)


class Conflict(Exception):
    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)


class Unauthorized(Exception):
    def __init__(self, message: str = "User unauthorized") -> None:
        super().__init__(message)


class Forbidden(Exception):
    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(message)
