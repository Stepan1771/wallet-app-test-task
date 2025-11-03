from typing import Sequence

from fastapi import HTTPException
from starlette import status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import (
    Wallet,
    Operation,
)
from core.schemas.operation import OperationCreate

from crud import operations as crud_operations

from utils import OperationUtils


async def get_all_wallets(
        session: AsyncSession,
) -> Sequence[Wallet]:
    try:
        stmt = await session.execute(
            select(Wallet)
            .order_by(Wallet.uuid)
        )
        wallets = stmt.scalars().all()
        if not wallets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallets not found",
            )
        return wallets

    except Exception as e:
        raise e


async def get_wallet_balance_by_uuid(
        session: AsyncSession,
        wallet_uuid: str,
) -> Wallet:
    try:
        stmt = await session.execute(
            select(Wallet)
            .filter(Wallet.uuid == wallet_uuid)
        )
        wallet = stmt.scalar_one_or_none()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet

    except Exception as e:
        raise e


async def get_wallet_operations(
        session: AsyncSession,
        wallet_uuid: str,
) -> Wallet:
    try:
        stmt = await session.execute(
            select(Wallet)
            .options(selectinload(Wallet.operations))
            .filter(Wallet.uuid == wallet_uuid)
        )
        wallet = stmt.scalar_one_or_none()
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found",
            )
        return wallet

    except Exception as e:
        raise e


async def create_wallet(
        session: AsyncSession,
) -> Wallet:
    try:
        wallet = Wallet()
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet

    except Exception as e:
        raise e


async def create_wallet_operation(
        session: AsyncSession,
        wallet_uuid: str,
        operation_schema: OperationCreate,
) -> (Wallet, Operation):
    try:
        stmt = await session.execute(
            select(Wallet)
            .filter(Wallet.uuid == wallet_uuid)
            .with_for_update()
        )
        wallet = stmt.scalar_one_or_none()
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found",
            )
        current_balance = float(wallet.balance)

        operation_utils = OperationUtils(
            operation_type=operation_schema.operation_type,
            wallet_balance=current_balance,
            amount=operation_schema.amount,
        )
        wallet.balance = operation_utils.execute_operation()
        await session.commit()

        operation = await crud_operations.create_operation(
                session=session,
                wallet_uuid=wallet_uuid,
                operation_type=operation_schema.operation_type,
                amount=operation_schema.amount,
        )
        await session.refresh(wallet)
        return wallet, operation

    except Exception as e:
        raise e


async def delete_wallet(
        session: AsyncSession,
        wallet_uuid: str,
) -> HTTPException:
    try:
        stmt = await session.execute(
            select(Wallet)
            .filter(Wallet.uuid == wallet_uuid)
        )
        result = stmt.scalar_one_or_none()

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found",
            )

        await session.delete(result)
        await session.commit()
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    except Exception as e:
        raise e








