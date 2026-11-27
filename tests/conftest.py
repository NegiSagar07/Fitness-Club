import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.database import Base, engine, AsyncSessionLocal, get_db_session # Assuming get_db is your dependency

# 1. This allows you to run async fixtures
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# tests/conftest.py

@pytest.fixture(scope="session", autouse=True, loop_scope="session")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(loop_scope="function")
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture
async def test_client(db_session):
    # 2. THE SECRET SAUCE: Override the 'get_db' dependency in your FastAPI app
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db
    
    # Use AsyncClient for async projects instead of TestClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # Clear overrides after the test is done
    app.dependency_overrides.clear()