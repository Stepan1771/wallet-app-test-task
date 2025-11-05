import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_delete_wallet_success(
        client: AsyncClient,
        sample_wallet,
):
    wallet_uuid = sample_wallet.uuid
    response = await client.request(
        "DELETE",
        "/api/v1/wallets/delete",
        json={"uuid": wallet_uuid},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_wallet_not_found(
        client: AsyncClient,
):
    wallet_uuid_fake = "fake-uuid"
    response = await client.request(
        "DELETE",
        "/api/v1/wallets/delete",
        json={"uuid": wallet_uuid_fake},
    )
    assert response.status_code == 404


