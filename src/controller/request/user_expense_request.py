from src.application.custom_base_model import CustomBaseModel
from src.domain import common
from src.domain import expense as domain


class UserExpense(CustomBaseModel):
    name: str
    user: common.ObjectID
    quantity: float
    datetime: common.AwareDatetime

    def to_domain(self) -> domain.UserExpense:
        return domain.UserExpense.model_validate(self.model_dump())