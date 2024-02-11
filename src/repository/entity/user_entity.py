from datetime import datetime

from pydantic import Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.application.custom_base_model import CustomBaseModel
from src.domain.user import GetUser


from datetime import datetime
from typing import Self

from pydantic import Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.application.custom_base_model import CustomBaseModel
from src.domain.user import RegisterUser

class RegisterUserEntity(CustomBaseModel):
    name: str
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birthday: datetime
    phone_number: PhoneNumber
    password: str

    @classmethod
    def from_domain(cls, user: RegisterUser) -> Self:
        name = f"{user.firstname} {user.lastname}"

        user_dictionary = user.model_dump()
        user_dictionary.update({"name": name})
        return cls.model_validate(user_dictionary)
    

class GetUserEntity(CustomBaseModel):
    id: str = Field(alias="_id")
    name: str
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birthday: datetime
    phone_number: PhoneNumber
    password: str

    def to_domain(self) -> GetUser:
        return GetUser.model_validate(self.model_dump())
