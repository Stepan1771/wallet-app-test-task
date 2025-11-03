from typing import List

from pydantic import BaseModel, ConfigDict

from core.schemas.operation import OperationResponse


class WalletBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class WalletResponse(WalletBase):
    uuid: str
    balance: float


class WalletOperationResponse(WalletBase):
    wallet: WalletResponse
    operation: OperationResponse

    model_config = ConfigDict(
        from_attributes=True,
    )


class WalletOperationsResponse(WalletBase):
    uuid: str
    balance: float
    operations: List[OperationResponse]


class WalletDelete(WalletBase):
    uuid: str






    





