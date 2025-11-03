from typing import List

from pydantic import BaseModel, ConfigDict

from core.schemas.operation import OperationResponse


class WalletBase(BaseModel):
    uuid: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class WalletResponse(WalletBase):
    balance: float


class WalletOperationResponse(WalletBase):
    balance: float
    operations: List[OperationResponse]


class WalletDelete(WalletBase):
    pass






    





