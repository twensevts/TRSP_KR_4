import pytest


@pytest.mark.asyncio
async def test_validated_user_accepts_correct_payload(client, faker_instance):
    payload = {
        "username": faker_instance.user_name(),
        "age": faker_instance.random_int(min=19, max=60),
        "email": faker_instance.email(),
        "password": faker_instance.password(length=12),
        "phone": faker_instance.phone_number(),
    }

    response = await client.post("/validated-users", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


@pytest.mark.asyncio
async def test_validated_user_returns_custom_validation_error(client, faker_instance):
    payload = {
        "username": faker_instance.user_name(),
        "age": 18,
        "email": "not-an-email",
        "password": "short",
    }

    response = await client.post("/validated-users", json=payload)
    assert response.status_code == 422

    body = response.json()
    assert body["detail"] == "Validation failed"
    fields = {issue["field"] for issue in body["errors"]}
    assert {"age", "email", "password"}.issubset(fields)
