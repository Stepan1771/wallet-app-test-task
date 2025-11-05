from datetime import datetime

from tests.mock_data import (
    get_mock_wallet,
    MockWallet,
    add_mock_wallet,
    delete_mock_wallet,
    MockOperation,
    add_mock_operation,
)
from fastapi import HTTPException

from starlette import status


async def mock_get_wallet_balance_by_uuid(
        session,
        wallet_uuid: str,
):
    wallet = get_mock_wallet(wallet_uuid)
    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet {wallet_uuid} not found",
        )

    return wallet


async def mock_create_wallet(
        session,
):
    wallet = MockWallet(balance=0)
    add_mock_wallet(wallet)
    return wallet


async def mock_get_all_wallets(
        session,
):
    wallet1 = MockWallet(
        balance=0,
    )
    wallet2 = MockWallet(
        balance=50.2,
    )
    wallet3 = MockWallet(
        balance=350.50,
    )
    add_mock_wallet(wallet1)
    add_mock_wallet(wallet2)
    add_mock_wallet(wallet3)
    return [wallet1, wallet2, wallet3]


async def mock_delete_wallet(
        session,
        wallet_uuid: str,
):
    wallet = get_mock_wallet(wallet_uuid)
    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet {wallet_uuid} not found",
        )
    delete_mock_wallet(wallet_uuid)
    return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
    )



async def mock_create_wallet_operation(
        session,
        wallet_uuid: str, operation_schema,
):
    wallet = get_mock_wallet(wallet_uuid)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found",
        )

    amount = str(operation_schema.amount)
    operation = MockOperation(
        uuid_wallet=wallet_uuid,
        description=amount,
    )

    if operation_schema.operation_type == "deposit":
        wallet.balance += float(str(operation_schema.amount))
        operation.operation = "deposit"
        operation.description = str(operation_schema.amount)
    elif operation_schema.operation_type == "withdraw":
        wallet.balance -= float(str(operation_schema.amount))
        operation.operation = "withdraw"
        operation.description = str(operation_schema.amount)

    add_mock_wallet(wallet)
    add_mock_operation(operation)

    return wallet, operation


async def mock_get_wallet_operations(
        session,
        wallet_uuid: str,
):
    wallet = get_mock_wallet(wallet_uuid)
    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet {wallet_uuid} not found",
        )

    operation1 = MockOperation(
        id=1,
        uuid_wallet=wallet_uuid,
        date_time=datetime.now(),
        operation="deposit",
        description="100",
    )
    operation2 = MockOperation(
        id=2,
        uuid_wallet=wallet_uuid,
        date_time=datetime.now(),
        operation="withdraw",
        description="100",
    )

    add_mock_wallet(wallet)
    add_mock_operation(operation1)
    add_mock_operation(operation2)
    wallet.operations = [operation1, operation2]
    return wallet



