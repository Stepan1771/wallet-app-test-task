import uuid
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from core.models import Wallet
from core.schemas.operation import OperationCreate

import utils


async def get_all_wallets(
        session: AsyncSession,
) -> Sequence[Wallet]:
    stmt = await session.execute(
        select(Wallet)
        .order_by(Wallet.uuid)
    )
    wallets = stmt.scalars().all()
    if not wallets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return wallets


async def get_wallet_balance_by_uuid(
        session: AsyncSession,
        uuid: str,
) -> Wallet:
    stmt = await session.execute(
        select(Wallet)
        .filter(Wallet.uuid == uuid)
    )
    wallet = stmt.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet


async def get_wallet_operations(
        session: AsyncSession,
        uuid: str,
) -> Wallet:
    stmt = await session.execute(
        select(Wallet)
        .options(selectinload(Wallet.operations))
        .filter(Wallet.uuid == uuid)
    )
    wallet = stmt.scalar_one_or_none()

    return wallet


async def create_wallet(
        session: AsyncSession,
):
    wallet = Wallet()
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    return wallet


async def create_operation(
        session: AsyncSession,
        uuid: str,
        operation_schema: OperationCreate,
):
    try:
        stmt = await session.execute(
            select(Wallet)
            .filter(Wallet.uuid == uuid)
            .with_for_update()
        )
        wallet = stmt.scalar_one_or_none()
        current_balance = float(wallet.balance)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if operation_schema.operation_type == "deposit":
            new_balance = utils.deposit(
                wallet_balance=current_balance,
                amount=operation_schema.amount,
            )
            wallet.balance = new_balance
            await session.commit()

        elif operation_schema.operation_type == "withdraw":
            new_balance = utils.withdraw(
                wallet_balance=current_balance,
                amount=operation_schema.amount,
            )
            wallet.balance = new_balance
            await session.commit()

        await session.refresh(wallet)

        return wallet

    except Exception as e:
        raise e


async def delete_wallet(
        session: AsyncSession,
        uuid: str,
):
    stmt = await session.execute(
        select(Wallet)
        .filter(Wallet.uuid == uuid)
    )
    result = stmt.scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Wallet not found")

    await session.delete(result)
    await session.commit()
    return {
        "status": "OK",
        "message": f"Wallet <{uuid}> deleted",
    }








