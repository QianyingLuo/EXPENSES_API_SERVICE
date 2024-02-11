from datetime import date
from typing import Optional, Self
import bson
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import EmailStr, Field
from src.application.custom_base_model import CustomBaseModel
from src.domain.user import user_register as domain


class RegisterUser(CustomBaseModel):
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber

    def to_domain(self) -> domain.PostRegisterUser:
        return domain.PostRegisterUser.model_validate(self.model_dump())
    
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