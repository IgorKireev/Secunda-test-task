class NotFoundError(Exception):
    def __init__(self, entity: str) -> None:
        self.entity =  entity
        self.detail = f"{entity} not found"
        super().__init__(self.detail)


class DataIntegrityError(Exception):
    def __init__(self, message: str = "Data integrity violation") -> None:
        super().__init__(message)