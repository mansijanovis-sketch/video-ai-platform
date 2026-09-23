import uuid

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import EarlyAccessSignup


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_early_access_rows():
    db = SessionLocal()
    try:
        db.query(EarlyAccessSignup).delete()
        db.commit()
    finally:
        db.close()

    yield

    db = SessionLocal()
    try:
        db.query(EarlyAccessSignup).delete()
        db.commit()
    finally:
        db.close()


def make_email(prefix="signup"):
    return f"{prefix}{uuid.uuid4().hex[:8]}@example.com"


def test_valid_registration():
    email = make_email("valid")

    response = client.post(
        "/api/early-access",
        json={"name": "Alice Johnson", "email": email},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["message"] == "Early access registration received."

    db = SessionLocal()
    try:
        signup = db.query(EarlyAccessSignup).filter(EarlyAccessSignup.email == email.lower()).first()
        assert signup is not None
        assert signup.name == "Alice Johnson"
    finally:
        db.close()


def test_invalid_email():
    response = client.post(
        "/api/early-access",
        json={"name": "Alice Johnson", "email": "not-an-email"},
    )

    assert response.status_code == 422


def test_missing_name():
    response = client.post(
        "/api/early-access",
        json={"name": "   ", "email": make_email("missing-name")},
    )

    assert response.status_code == 422


def test_duplicate_email():
    email = make_email("duplicate")

    first = client.post(
        "/api/early-access",
        json={"name": "Alice Johnson", "email": email},
    )
    assert first.status_code == 200

    second = client.post(
        "/api/early-access",
        json={"name": "Alice Johnson", "email": email.upper()},
    )

    assert second.status_code == 200
    payload = second.json()
    assert payload["success"] is True
    assert payload["message"] == "This email is already registered for early access."

    db = SessionLocal()
    try:
        count = db.query(EarlyAccessSignup).filter(EarlyAccessSignup.email == email.lower()).count()
        assert count == 1
    finally:
        db.close()


def test_database_persistence():
    email = make_email("persist")

    client.post(
        "/api/early-access",
        json={"name": "Persistent User", "email": email},
    )

    db = SessionLocal()
    try:
        signup = db.query(EarlyAccessSignup).filter(EarlyAccessSignup.email == email.lower()).first()
        assert signup is not None
        assert signup.name == "Persistent User"
        assert signup.created_at is not None
    finally:
        db.close()


def test_endpoint_availability():
    response = client.post(
        "/api/early-access",
        json={"name": "Available Route", "email": make_email("available")},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
