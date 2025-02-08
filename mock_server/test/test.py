from starlette.testclient import TestClient
from api_server.app.db import database
from api_server.app.main import app
import json

client = TestClient(app)

users = database.generate_user_db()

def test_get_stores():
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == users

def test_get_store():
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json() == users[0]

"""
def test_add_store():
    body = {"id": 100, "name":"TestUser", "email": "test.user@example.com"}
    body = json.dumps(body)
    response = client.post('/users', data=body)
    assert response.status_code == 201
"""

def test_delete_store():
    response = client.delete('/users/1')
    assert response.status_code == 201
