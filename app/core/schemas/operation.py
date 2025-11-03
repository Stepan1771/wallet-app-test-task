from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class OperationResponse(BaseModel):
    id: int
    uuid_wallet: str
    date_time: datetime
    operation: str
    description: str

    model_config = ConfigDict(
        from_attributes=True
    )


class OperationCreate(BaseModel):
    operation_type: str
    amount: float

    @field_validator("operation_type")
    def validate_operation(cls, value):
        value = value.strip().lower()
        if value not in ["deposit", "withdraw"]:
            raise ValueError("Invalid operation")
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        if value < 1:
            raise ValueError("Invalid amount")
        return value


