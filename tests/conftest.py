import pytest

from datetime import datetime
from bson.objectid import ObjectId
from random import randint
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def test_client():

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def tag():
    """Generate a random tag number."""
    return str(randint(10000, 99999))


@pytest.fixture()
def device_payload(tag):
    """Generate a device payload."""
    return {
        "tag": tag,
        "vendor": "Acme Sensor Co.",
        "model": "Super Device 9000"
    }


@pytest.fixture()
def device_payload_updated(tag):
    """Generate an updated devuce payload."""
    return {
        "tag": tag,
        "vendor": "Generic Sensing Ltd.",
        "model": "Fantastic Mystery Machine"
    }


@pytest.fixture()
def object_id():
    """Generate a random uuid."""
    return str(ObjectId())


@pytest.fixture()
def sensor_payload(object_id, tag):
    """Generate a sensor payload."""
    return {
        "device": object_id,
        "measurement": "Air Temperature"
    }


@pytest.fixture()
def sensor_payload_updated(object_id, tag):
    """Generate an updated sensor payload."""
    return {
        "device": object_id,
        "tag": tag,
        "measurement": "Soil Temperature"
    }


@pytest.fixture()
def sample_payload(object_id):
    """Generate a sample payload."""
    return {
        "sensor": object_id,
        "timestamp": str(datetime.now()),
        "value": float(randint(10000, 99999)),
        "predicted": False
    }
