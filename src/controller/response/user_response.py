from datetime import date
from typing import Self
from pydantic import EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.application.custom_base_model import CustomBaseModel
from src.domain import user as domain



class GetUserResponse(CustomBaseModel):
    id: str
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber

    @classmethod
    def to_response(cls, user: domain.GetUser) -> Self:
        return cls.model_validate(user.model_dump())
    

class LoginResultResponse(CustomBaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    token: str

    @classmethod
    def to_response(cls, login_credentials: domain.LoginResult) -> Self:
        return cls.model_validate(login_credentials.model_dump())

