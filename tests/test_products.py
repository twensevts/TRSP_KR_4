import pytest


@pytest.mark.asyncio
async def test_product_create_and_fetch(client, faker_instance):
    payload = {
        "title": faker_instance.word(),
        "price": "19.99",
        "count": 5,
        "description": faker_instance.sentence(),
    }

    create_response = await client.post("/products", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == payload["title"]
    assert created["description"] == payload["description"]

    get_response = await client.get(f"/products/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]
