from datetime import datetime

from pydantic import Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.application.custom_base_model import CustomBaseModel
from src.domain.user.user_register import GetUser

class GetUserEntity(CustomBaseModel):
    id: str = Field(alias="_id")
    name: str
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birthday: datetime
    phone_number: PhoneNumber

    def to_domain(self) -> GetUser:
        return GetUser.model_validate(self.model_dump())
