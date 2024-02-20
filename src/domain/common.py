from typing import Annotated, NewType

import pydantic
from src.application.custom_base_model import CustomBaseModel

from datetime import datetime, timezone

def to_datetime_str(dt: datetime) -> str:
    if not dt.tzinfo:
        raise TimeZoneNotFound()
    
    utc_dt = dt.astimezone(timezone.utc)

    return f"{utc_dt.year:04}" + utc_dt.strftime("-%m-%dT%H:%M:%SZ")

ObjectID = NewType("ObjectID", pydantic.constr(pattern=r"^[0-9a-fA-F]{24}$"))

MiimetiqName = NewType(
    "MiimetiqName", pydantic.constr(pattern=r"^[a-zA-Z0-9:@&_ \-\(\)\[\]]+$")
)

AwareDatetime = Annotated[
    pydantic.AwareDatetime,
    pydantic.PlainSerializer(to_datetime_str, return_type=str, when_used="json"),
]

class CreationResponse(CustomBaseModel):
    id: str
    acknowledged: bool

class UserAlreadyExists(Exception): ...

class UserNotFound(Exception): ...

class InvalidCredentials(Exception): ...

class ExpenseAlreadyExists(Exception): ...

class ExpenseNotFound(Exception): ...

class GenericHTTPException(CustomBaseModel):
    status_code: str
    type: str 
    detail: str

class TimeZoneNotFound(Exception): ...


def now() -> datetime:
    return datetime.now(timezone.utc)