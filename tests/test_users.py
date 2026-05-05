import pytest


@pytest.mark.asyncio
async def test_create_get_delete_user_cycle(client, faker_instance):
    payload = {
        "username": faker_instance.user_name(),
        "age": faker_instance.random_int(min=19, max=75),
    }

    create_response = await client.post("/users", json=payload)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["username"] == payload["username"]
    assert created_user["age"] == payload["age"]
    assert isinstance(created_user["id"], int)

    user_id = created_user["id"]

    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json() == created_user

    delete_response = await client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    missing_response = await client.get(f"/users/{user_id}")
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_missing_user_returns_404(client):
    response = await client.delete("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
