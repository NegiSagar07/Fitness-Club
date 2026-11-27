"""
Tests for user-related endpoints
"""

import pytest

@pytest.fixture
@pytest
async def test_user():
    return {"id": 1, "username": "testuser", "email": "testuser@example.com"}


@pytest.mark.asyncio
async def test_create_user(test_client, test_user):
    response = await test_client.post("/users/", json=test_user)
    assert response.status_code == 201
    assert response.json() == test_user     


@pytest.mark.asyncio
async def test_get_user(test_client, test_user):
    response = await test_client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json() == test_user


@pytest.mark.asyncio
async def test_update_user(test_client, test_user):
    updated_user = test_user.copy()
    updated_user["username"] = "updateduser"
    response = await test_client.put(f"/users/{test_user['id']}", json=updated_user)
    assert response.status_code == 200
    assert response.json() == updated_user


@pytest.mark.asyncio
async def test_delete_user(test_client, test_user):
    response = await test_client.delete(f"/users/{test_user['id']}")
    assert response.status_code == 204
    # Verify that the user has been deleted
    response = await test_client.get(f"/users/{test_user['id']}")
    assert response.status_code == 404

