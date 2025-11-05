import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from main import main_app as app

from tests.mock_data import (
    reset_mock_db,
    add_mock_wallet,
    MockWallet,
    MockOperation,
    add_mock_operation,
)


@pytest.fixture(scope="session")
def event_loop_policy():
    import asyncio
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    return asyncio.get_event_loop_policy()


@pytest.fixture(autouse=True)
def clear_mock_db():
    reset_mock_db()
    yield
    reset_mock_db()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:

    from tests.mock_crud import (
        mock_get_wallet_balance_by_uuid,
        mock_create_wallet,
        mock_get_all_wallets,
        mock_delete_wallet,
        mock_create_wallet_operation,
        mock_get_wallet_operations
    )

    with patch(
            "crud.wallets.get_wallet_balance_by_uuid",
            mock_get_wallet_balance_by_uuid
    ), patch(
        "crud.wallets.create_wallet",
        mock_create_wallet
    ), patch(
        "crud.wallets.get_all_wallets",
        mock_get_all_wallets
    ), patch(
        "crud.wallets.delete_wallet",
        mock_delete_wallet
    ), patch(
        "crud.wallets.create_wallet_operation",
        mock_create_wallet_operation
    ), patch(
        "crud.wallets.get_wallet_operations",
        mock_get_wallet_operations
    ):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as ac:
            yield ac


@pytest.fixture
def sample_wallet():
    wallet = MockWallet(
        balance=1000,
    )
    add_mock_wallet(wallet)
    return wallet


@pytest.fixture
def sample_operation():
    operation = MockOperation()
    add_mock_operation(operation)
    return operation


@pytest.fixture
def empty_wallet():
    wallet = MockWallet(balance=0)
    add_mock_wallet(wallet)
    return wallet

