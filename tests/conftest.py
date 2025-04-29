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
def convert_timestamp():
    """Cut last seven digits of timestamp as we don't need that accuracy"""
    def inner_convert_timestamp(server, local):
        server_ts = datetime.strptime(server[:-7], "%Y-%m-%dT%H:%M:%S")
        local_ts = datetime.strptime(local[:-7], "%Y-%m-%d %H:%M:%S")
        return server_ts, local_ts
    return inner_convert_timestamp


@pytest.fixture()
def animal_payload():
    """Generate an animal payload."""
    return {
        "identifier": "UK230011200123",
        "specie": "Cattle",
        "gender": "Female",
        "birthDate": "2025-04-24 12:18:06.625573",
        "productionPurpose": "Milk",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "Healthy"
        }


@pytest.fixture()
def animal_payload_updated():
    """Generate an animal payload."""
    return {
        "identifier": "UK230011200123",
        "specie": "Cattle",
        "gender": "Male",
        "birthDate": "2025-04-24 12:18:06.625573",
        "productionPurpose": "Wool",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "InTreatment"
        }


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
    """Generate an updated device payload."""
    return {
        "tag": tag,
        "vendor": "Generic Sensing Ltd.",
        "model": "Fantastic Mystery Machine"
    }


@pytest.fixture()
def weight_payload():
    """Generate a weight event payload."""
    return {
        "animal": str(ObjectId()),
        "weight": {
            "measurement": float(randint(453, 816)),
            "units": "KGM",
            "method": "LoadCell",
            "resolution": float(randint(1, 9)/10)
        },
        "device": str(ObjectId()),
        "timeOffFeed": float(randint(1, 5)),
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
