import uuid

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all_wallets(client: AsyncClient):
    """Тест получения всех кошельков"""
    response = await client.get(
        "/api/v1/wallets/all",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_create_wallet(client: AsyncClient):
    """Тест создания кошелька"""
    response = await client.post(
        "/api/v1/wallets/create-wallet",
    )
    assert response.status_code == 201
    data = response.json()
    assert data["balance"] == 0.0
    assert len(data["uuid"]) == 36


@pytest.mark.asyncio
async def test_get_wallet_balance(client: AsyncClient, test_wallet):
    """Тест получения баланса кошелька"""
    response = await client.get(f"/api/v1/wallets/{test_wallet.uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == test_wallet.uuid
    assert data["balance"] == test_wallet.balance