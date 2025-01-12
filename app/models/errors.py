from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

class NotFoundError(ErrorResponse):
    detail: str = "Resource not found"

class ValidationError(ErrorResponse):
    detail: str = "Validation error"

class UnauthorizedError(ErrorResponse):
    detail: str = "Unauthorized access"

class InternalServerError(ErrorResponse):
    detail: str = "Internal server error"