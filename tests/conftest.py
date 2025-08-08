from datetime import datetime, timezone
from random import randint

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from app.main import app

from . import common


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
        "identifier": {"id": "UK230011200123", "scheme": "gov.uk"},
        "specie": "Cattle",
        "gender": "Female",
        "birthDate": "2025-04-24 12:18:06.625573",
        "productionPurpose": "Milk",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "Healthy",
        "resourceType": "icarAnimalCoreResource",
    }


@pytest.fixture()
def animal_payload_updated():
    """Generate an animal payload."""
    return {
        "identifier": {"id": "UK230011200124", "scheme": "gov.uk"},
        "specie": "Cattle",
        "gender": "Male",
        "productionPurpose": "Wool",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "InTreatment",
        "resourceType": "icarAnimalCoreResource",
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
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "weight": {
            "measurement": float(randint(453, 816)),
            "units": "KGM",
            "method": "LoadCell",
            "resolution": float(randint(1, 9) / 10),
        },
        "device": {"manufacturerName": "Acme Sensor Co."},
        "timeOffFeed": float(randint(1, 5)),
        "resourceType": "icarWeightEventResource",
    }


@pytest.fixture()
def feed_intake_payload():
    """Generate a feed intake event payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "feedingStartingDateTime": datetime.now(timezone.utc).isoformat(),
        "feedVisitDuration": {"unitCode": "MIN", "value": 10},
        "consumedFeed": [
            {"feedId": {"id": "test", "scheme": "ft.org"}, "dryMatterPercentage": 10}
        ],
        "resourceType": "icarFeedIntakeEventResource",
    }


@pytest.fixture()
def withdrawal_payload():
    """Generate a withdrawal payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "endDateTime": datetime.now(timezone.utc).isoformat(),
        "productType": "Eggs",
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def carcass_payload():
    """Generate a withdrawal payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "side": "Left",
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def health_status_payload():
    """Generate a health status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "observedStatus": "Healthy",
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def lactation_status_payload():
    """Generate a lactation status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "observedStatus": "Open",
        "eventDateTime": datetime.now(timezone.utc).isoformat(),
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def position_payload():
    """Generate a position payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "positionName": "Yard",
        "eventDateTime": datetime.now(timezone.utc).isoformat(),
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def repro_status_payload():
    """Generate a repro status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "observedStatus": "Pregnant",
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def attention_payload():
    """Generate a repro status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "category": "Health",
        "causes": ["Activity", "LyingTooLong"],
        "priority": "Urgent",
        "resourceType": "icarWithdrawalEventResource",
    }


@pytest.fixture()
def object_id():
    """Generate a random uuid."""
    return str(ObjectId())


@pytest.fixture()
def sensor_payload(object_id, serial):
    """Generate a sensor payload."""
    return {"device": object_id, "measurement": "Air Temperature"}


@pytest.fixture()
def sensor_payload_updated(object_id, serial):
    """Generate an updated sensor payload."""
    return {"device": object_id, "serial": serial, "measurement": "Soil Temperature"}


@pytest.fixture()
def sample_payload(object_id):
    """Generate a sample payload."""
    return {
        "sensor": object_id,
        "timestamp": str(datetime.now()),
        "value": float(randint(10000, 99999)),
        "predicted": False,
    }


@pytest.fixture()
def machine_payload():
    """Generate a machine payload."""
    return {
        "manufacturer": "Acme Machine Co.",
        "model": "Machine 3000",
        "type": ["Vehicle", "Off-Road", "Utility"],
        "registration": "BD51 SMR",
    }


@pytest.fixture()
def conformation_payload(object_id):
    """Generate a conformation payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "traitGroup": "Composite",
        "score": 47,
        "traitScored": "BodyLength",
        "method": "Automated",
        "resourceType": "icarConformationScoreEvent",
    }


@pytest.fixture()
def drying_off_payload(object_id):
    """Generate a drying off payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "resourceType": "icarMilkingDryOffEventResource",
    }


@pytest.fixture()
def milking_visit_payload(object_id):
    """Generate a milking visit payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "milkingStartingDateTime": str(datetime.now()),
        "milkingMilkWeight": {"unitCode": "KGM", "value": 10},
        "resourceType": "icarMilkingVisitEventResource",
    }


@pytest.fixture()
def arrival_payload(object_id):
    """Generate an arrival payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "arrivalReason": "ShowReturn",
        "animalState": {
            "currentLactationParity": 2,
            "lastCalvingDate": datetime.now(timezone.utc).isoformat(),
        },
        "resourceType": "icarMovementArrivalEventResource",
    }


@pytest.fixture()
def birth_payload(object_id):
    """Generate a birth payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "registrationReason": "Born",
        "resourceType": "icarMovementBirthEventResource",
    }


@pytest.fixture()
def death_payload(object_id):
    """Generate a death payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "deathReason": "Age",
        "resourceType": "icarMovementDeathEventResource",
    }


@pytest.fixture()
def departure_payload(object_id):
    """Generate an departure payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "gov.uk"},
        "departureReason": "Sale",
        "departureKind": "Sale",
        "resourceType": "icarMovementDepartureEventResource",
    }


@pytest.fixture()
def machine_payload_updated():
    """Generate an updated machine payload."""
    return {
        "manufacturer": "Generic Machine Ltd.",
        "model": "IronHorse XT-450",
        "type": ["Vehicle", "Tractor"],
    }
