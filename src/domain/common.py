from typing import Literal
from src.application.custom_base_model import CustomBaseModel
from fastapi import status

class CreationResponse(CustomBaseModel):
    id: str
    acknowledged: bool

class UserAlreadyExists(Exception): ...

class UserNotFound(Exception): ...

class InvalidCredentials(Exception): ...

class GenericHTTPException(CustomBaseModel):
    status_code: str
    type: str 
    detail: str