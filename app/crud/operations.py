from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Operation


async def create_operation(
        session: AsyncSession,
        wallet_uuid: str,
        operation_type: str,
        amount: float,
) -> Operation:
    try:
        operation = Operation(
            uuid_wallet=wallet_uuid,
            date_time=datetime.now(),
            operation=operation_type,
            description=str(amount),
        )
        session.add(operation)
        await session.commit()
        await session.refresh(operation)
        return operation

    except Exception as e:
        raise e
