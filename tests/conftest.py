import pytest


from random import randint
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def test_client():

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def device_tag():
    """Generate a random user id."""
    return str(randint(10000, 99999))


@pytest.fixture()
def device_payload(device_tag):
    """Generate a user payload."""
    return {
        "tag": device_tag,
        "vendor": "Acme Sensor Co.",
        "model": "Super Device 9000"
    }


@pytest.fixture()
def device_payload_updated(device_tag):
    """Generate an updated user payload."""
    return {
        "tag": device_tag,
        "vendor": "Generic Sensing Ltd.",
        "model": "Fantastic Mystery Machine"
    }
