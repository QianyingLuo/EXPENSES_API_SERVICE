from typing import NewType

import pydantic
from src.application.custom_base_model import CustomBaseModel

ObjectID = NewType("ObjectID", pydantic.constr(pattern=r"^[0-9a-fA-F]{24}$"))

MiimetiqName = NewType(
    "MiimetiqName", pydantic.constr(pattern=r"^[a-zA-Z0-9:@&_ \-\(\)\[\]]+$")
)

class CreationResponse(CustomBaseModel):
    id: str
    acknowledged: bool

class UserAlreadyExists(Exception): ...

class UserNotFound(Exception): ...

class InvalidCredentials(Exception): ...

class ExpenseAlreadyExists(Exception): ...

class GenericHTTPException(CustomBaseModel):
    status_code: str
    type: str 
    detail: str