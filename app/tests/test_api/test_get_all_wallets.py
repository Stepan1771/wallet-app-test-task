import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_wallets_success(
        client: AsyncClient,
):
    response = await client.get(f"/api/v1/wallets/all")
    assert response.status_code == 200
    data = response.json()
