import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_wallet_operations_success(
        client: AsyncClient,
        sample_wallet,
):
    wallet_uuid = sample_wallet.uuid
    response = await client.get(
        f"/api/v1/wallets/{wallet_uuid}/wallet-operations",
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_wallet_operations_not_found(
        client: AsyncClient,
):
    wallet_uuid_fake = "fake-uuid"
    response = await client.get(
        f"/api/v1/wallets/{wallet_uuid_fake}/wallet-operations",
    )
    assert response.status_code == 404