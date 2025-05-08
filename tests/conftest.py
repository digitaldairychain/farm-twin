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
def serial():
    """Generate a random serial number."""
    return str(randint(10000, 99999))


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
        "productionPurpose": "Wool",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "InTreatment"
    }


@pytest.fixture()
def device_payload(serial):
    """Generate a device payload."""
    return {
        "id": "Sample",
        "serial": serial,
        "softwareVersion": "1.3",
        "manufacturer": {
            "id": "Acme Sensor Co.",
        },
        "isActive": True,
    }


@pytest.fixture()
def device_payload_updated(serial):
    """Generate an updated device payload."""
    return {
        "id": "Revised Sample",
        "serial": serial,
        "softwareVersion": "1.4",
        "hardwareVersion": "1.0",
        "manufacturer": {
            "id": "Generic Sensing Ltd.",
            "deviceType": "Fantastic Mystery Machine",
        },
        "isActive": False,
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
def sensor_payload(object_id, serial):
    """Generate a sensor payload."""
    return {
        "device": object_id,
        "measurement": "Air Temperature"
    }


@pytest.fixture()
def sensor_payload_updated(object_id, serial):
    """Generate an updated sensor payload."""
    return {
        "device": object_id,
        "serial": serial,
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


@pytest.fixture()
def machine_payload():
    """Generate a machine payload."""
    return {
        "manufacturer": "Acme Machine Co.",
        "model": "Machine 3000",
        "type": ["Vehicle", "Off-Road", "Utility"],
        "registration": "BD51 SMR"
    }


@pytest.fixture()
def machine_payload_updated():
    """Generate an updated machine payload."""
    return {
        "manufacturer": "Generic Machine Ltd.",
        "model": "IronHorse XT-450",
        "type": ["Vehicle", "Tractor"]
    }
