from src.application.custom_base_model import CustomBaseModel
from src.domain import common
from src.domain import expense as domain
from datetime import datetime

class CreateExpense(CustomBaseModel):
    name: str

    def to_domain(self) -> domain.CreateExpense:
        return domain.CreateExpense.model_validate(self.model_dump())
    

class UserExpense(CustomBaseModel):
    name: str
    user: common.ObjectID
    quantity: float
    datetime: common.AwareDatetime

    def to_domain(self) -> domain.UserExpense:
        return domain.UserExpense.model_validate(self.model_dump())