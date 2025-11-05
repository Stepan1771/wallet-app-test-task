import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_wallet_success(
        client: AsyncClient,
):
    response = await client.post(f"/api/v1/wallets/create-wallet")
    assert response.status_code == 201
    data = response.json()
    assert "uuid" in data
    assert "balance" in data
    assert len(data["uuid"]) == 36
    assert data["balance"] == 0.0