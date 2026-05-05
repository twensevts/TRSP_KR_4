import pytest


@pytest.mark.asyncio
async def test_custom_exception_a_handler(client):
    response = await client.get("/errors/a")
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Business rule failed",
        "error_code": "RULE_A",
    }


@pytest.mark.asyncio
async def test_custom_exception_b_handler(client):
    response = await client.get("/errors/b")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Target resource was not found",
        "error_code": "RULE_B",
    }
