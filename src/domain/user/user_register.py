from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import EmailStr
from src.application.custom_base_model import CustomBaseModel


class PostRegisterUser(CustomBaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber

class GetUser(CustomBaseModel):
    id: str
    name: str
    firstname: str
    lastname: str
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber