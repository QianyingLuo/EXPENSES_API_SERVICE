from datetime import date
from pydantic import EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.application.custom_base_model import CustomBaseModel
from src.domain import user as domain


class RegisterUserRequest(CustomBaseModel):
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birthday: date
    phone_number: PhoneNumber
    password: str = Field(min_length=6, max_length=20)

    def to_domain(self) -> domain.RegisterUser:
        return domain.RegisterUser.model_validate(self.model_dump())
    

    
class LoginCredentialsRequest(CustomBaseModel):
    email: EmailStr
    password: str

    def to_domain(self) -> domain.LoginCredentials:
        return domain.LoginCredentials.model_validate(self.model_dump())