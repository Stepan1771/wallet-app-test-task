import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_wallet_balance_success(
        client: AsyncClient,
        sample_wallet,
):
    wallet_uuid = sample_wallet.uuid
    response = await client.get(
        f"/api/v1/wallets/{wallet_uuid}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == wallet_uuid
    assert data["balance"] == 1000


@pytest.mark.asyncio
async def test_get_wallet_balance_not_found(
        client: AsyncClient,
):
    fake_uuid = str(uuid4())
    response = await client.get(
        f"/api/v1/wallets/{fake_uuid}",
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_get_wallet_with_zero_balance(
        client: AsyncClient,
        empty_wallet,
):
    wallet_uuid = empty_wallet.uuid
    response = await client.get(
        f"/api/v1/wallets/{wallet_uuid}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 0


@pytest.mark.asyncio
async def test_wallet_response_structure(
        client: AsyncClient,
        sample_wallet,
):
    wallet_uuid = sample_wallet.uuid
    response = await client.get(
        f"/api/v1/wallets/{wallet_uuid}",
    )
    assert response.status_code == 200
    data = response.json()
    required_fields = ["uuid", "balance"]
    for field in required_fields:
        assert field in data
    assert isinstance(data["uuid"], str)
    assert isinstance(data["balance"], float)


@pytest.mark.asyncio
async def test_wallet_with_large_balance(
        client: AsyncClient,
):
    from tests.mock_data import MockWallet, add_mock_wallet

    large_balance = 999_999_999_999
    wallet = MockWallet(balance=large_balance)
    add_mock_wallet(wallet)
    response = await client.get(
        f"/api/v1/wallets/{wallet.uuid}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == large_balance
