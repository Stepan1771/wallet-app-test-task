import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_wallet_operation_deposit_success(
        client: AsyncClient,
        sample_wallet,
):
    wallet_uuid = sample_wallet.uuid
    deposit_amount = float(100)
    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operation_type": "deposit",
            "amount": str(deposit_amount),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "operation" in data
    assert "wallet" in data


@pytest.mark.asyncio
async def test_create_wallet_operation_withdraw_success(
        client: AsyncClient,
        sample_wallet,
):
    wallet_uuid = sample_wallet.uuid
    withdraw_amount = float(100)
    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operation_type": "withdraw",
            "amount": str(withdraw_amount),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "operation" in data
    assert "wallet" in data


@pytest.mark.asyncio
async def test_create_wallet_operation_deposit_not_found(
        client: AsyncClient,
):
    wallet_uuid_fake = "fake-uuid"
    withdraw_amount = float(100)
    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid_fake}/operation",
        json={
            "operation_type": "deposit",
            "amount": str(withdraw_amount),
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_wallet_operation_withdraw_not_found(
        client: AsyncClient,
):
    wallet_uuid_fake = "fake-uuid"
    withdraw_amount = float(100)
    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid_fake}/operation",
        json={
            "operation_type": "withdraw",
            "amount": str(withdraw_amount),
        },
    )
    assert response.status_code == 404

