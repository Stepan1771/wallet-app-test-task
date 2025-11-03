from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.schemas.operation import OperationCreate
from core.schemas.wallet import WalletResponse, WalletDelete, WalletBase, WalletOperationResponse
from database import db_helper

from crud import wallets as crud_wallets


router = APIRouter(
    prefix=settings.api.v1.wallets,
    tags=["Wallets"],
)


@router.get(
    "/all",
    response_model=List[WalletResponse],
    summary="Получить все кошельки"
)
async def get_all_wallets(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    wallets = await crud_wallets.get_all_wallets(
        session=session,
    )
    return [
        WalletResponse.model_validate(wallet)
        for wallet in wallets
    ]


@router.get(
    "/{wallet_uuid}",
    response_model=WalletResponse,
    summary="Получить баланс кошелька по UUID",
)
async def get_wallet_balance(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        wallet_uuid: str = Path(..., description="Wallet UUID"),
):
    wallet = await crud_wallets.get_wallet_balance_by_uuid(
        session=session,
        uuid=wallet_uuid,
    )
    return WalletResponse.model_validate(wallet)


@router.post(
    "/create-wallet",
    response_model=WalletResponse,
    summary="Создать кошелек",
)
async def create_wallet(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    wallet = await crud_wallets.create_wallet(session=session)
    return WalletResponse.model_validate(wallet)


@router.post(
    "/{wallet_uuid}/operation",
    response_model=WalletResponse,
    summary="Создать операцию кошелька",
)
async def create_wallet_operation(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        operation_schema: OperationCreate,
        wallet_uuid: str = Path(..., description="Wallet UUID"),
):
    wallet = await crud_wallets.create_operation(
        session=session,
        uuid=wallet_uuid,
        operation_schema=operation_schema,
    )
    return WalletResponse.model_validate(wallet)


@router.get(
    "/{wallet_uuid}/wallet-operations",
    response_model=WalletOperationResponse,
    summary="Получить все операции кошелька по UUID",
)
async def get_wallet_operations(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        wallet_uuid: str = Path(..., description="Wallet UUID"),
):
    wallet = await crud_wallets.get_wallet_operations(
        session=session,
        uuid=wallet_uuid,
    )
    return WalletOperationResponse.model_validate(wallet)


@router.delete("/delete", summary="Удалить кошелек по UUID")
async def delete_wallet(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        delete_schema: WalletDelete
):
    result = await crud_wallets.delete_wallet(
        session=session,
        uuid=delete_schema.uuid,
    )
    return result