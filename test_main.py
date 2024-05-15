import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import SQLModel, get_db
from main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        return session


@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        return session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


def test_get_makes(client):
    res = client.post("/makes", params={"new_make_name": "BMW"})
    print(res)
    response = client.get("/makes")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "BMW"


def test_get_transmission(client):
    response = client.get("/transmissions")
    assert response.json() == []


def test_add_transmission(client):
    response = client.get("/transmissions")
    assert response.json() == []
    response = client.post("/transmissions", json={"name": "string", "type": "string"})
    assert response.status_code == 200
    response = client.get("/transmissions")
    data = response.json()
    assert data[0]["name"] == "string"


def test_update_transmission(client):
    response = client.get("/transmissions")
    assert response.json() == []
    response = client.post("/transmissions", json={"name": "string", "type": "string"})
    assert response.status_code == 200
    response = client.get("/transmissions")
    data = response.json()
    assert data[0]["name"] == "string"
    assert data[0]["id"] == 1
    response = client.put(
        "/transmissions/string", json={"name": "updated", "type": "updated"}
    )
    assert response.status_code == 200
    response = client.get("/transmissions")
    data = response.json()
    assert data[0]["id"] == 1
    assert data[0]["name"] == "updated"
    assert data[0]["type"] == "updated"


def test_delete_transmission(client):
    response = client.post("/transmissions", json={"name": "string", "type": "string"})
    assert response.status_code == 200
    response = client.get("/transmissions")
    data = response.json()
    assert data[0]["name"] == "string"
    response = client.delete("/transmissions/string")
    assert response.status_code == 200
    response = client.get("/transmissions")
    assert response.json() == []
