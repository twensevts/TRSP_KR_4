import pytest
import pytest_asyncio
from faker import Faker
from httpx import ASGITransport, AsyncClient

from app.database import Base, engine
from app.main import app, users_db


@pytest.fixture()
def faker_instance() -> Faker:
    return Faker()


@pytest_asyncio.fixture()
async def client():
    users_db.clear()
    Base.metadata.create_all(bind=engine)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
    Base.metadata.drop_all(bind=engine)
    users_db.clear()
