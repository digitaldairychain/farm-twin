from datetime import date, datetime, timedelta, timezone
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
        "identifier": {"id": "UK230011200123", "scheme": "uk.gov"},
        "specie": "Cattle",
        "gender": "Female",
        "birthDate": "2025-04-24 12:18:06.625573",
        "productionPurpose": "Milk",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "Healthy",
    }


@pytest.fixture()
def animal_payload_updated():
    """Generate an animal payload."""
    return {
        "identifier": {"id": "UK230011200124", "scheme": "uk.gov"},
        "specie": "Cattle",
        "gender": "Male",
        "productionPurpose": "Wool",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "InTreatment",
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
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "weight": {
            "measurement": float(randint(453, 816)),
            "units": "KGM",
            "method": "LoadCell",
            "resolution": float(randint(1, 9) / 10),
        },
        "device": {"manufacturerName": "Acme Sensor Co."},
        "timeOffFeed": float(randint(1, 5)),
    }


@pytest.fixture()
def group_weight_payload(object_id):
    """Generate a group weight event payload."""
    return {
        "groupMethod": "EmbeddedAnimalSet",
        "embeddedAnimalSet": {
            "id": object_id,
            "member": [{"id": "UK230011200123", "scheme": "uk.gov"}],
        },
        "statistics": [
            {
                "unit": "KGM",
                "aggregation": "Average",
                "value": float(randint(453, 816)),
            }
        ],
        "units": "KGM",
        "method": "LoadCell",
        "resolution": float(randint(1, 9) / 10),
        "device": {"manufacturerName": "Acme Sensor Co."},
        "timeOffFeed": float(randint(1, 5)),
    }


@pytest.fixture()
def feed_intake_payload():
    """Generate a feed intake event payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "feedingStartingDateTime": datetime.now(timezone.utc).isoformat(),
        "feedVisitDuration": {"unitCode": "MIN", "value": 10},
        "consumedFeed": [
            {"feedId": {"id": "test", "scheme": "ft.org"}, "dryMatterPercentage": 10}
        ],
    }


@pytest.fixture()
def withdrawal_payload():
    """Generate a withdrawal payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "endDateTime": datetime.now(timezone.utc).isoformat(),
        "productType": "Eggs",
    }


@pytest.fixture()
def carcass_payload():
    """Generate a withdrawal payload."""
    return {"animal": {"id": "UK230011200123", "scheme": "uk.gov"}, "side": "Left"}


@pytest.fixture()
def health_status_payload():
    """Generate a health status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "observedStatus": "Healthy",
    }


@pytest.fixture()
def lactation_status_payload():
    """Generate a lactation status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "observedStatus": "Fresh",
        "eventDateTime": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture()
def position_payload():
    """Generate a position payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "positionName": "Yard",
        "eventDateTime": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture()
def repro_status_payload():
    """Generate a repro status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "observedStatus": "Pregnant",
    }


@pytest.fixture()
def repro_abortion_payload():
    """Generate a repro abortion payload."""
    return {"animal": {"id": "UK230011200123", "scheme": "uk.gov"}}


@pytest.fixture()
def repro_do_not_breed_payload():
    """Generate a repro do not breed payload."""
    return {"animal": {"id": "UK230011200123", "scheme": "uk.gov"}, "doNotBreed": True}


@pytest.fixture()
def repro_heat_payload():
    """Generate a repro heat payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "heatDetectionMethod": "Visual",
        "certainty": "Suspect",
        "commencementDateTime": str(datetime.now() - timedelta(days=1)),
        "expirationDateTime": str(datetime.now() + timedelta(days=1)),
    }


@pytest.fixture()
def repro_insemination_payload():
    """Generate a repro insemination payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "inseminationType": "NaturalService",
        "sireOfficialName": "Frankel",
        "eventDateTime": str(datetime.now()),
    }


@pytest.fixture()
def repro_mating_recommendation_payload():
    """Generate a repro mating recommendation payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "sireRecommendations": [
            {
                "recommendationType": "SireRecommended",
                "sireIdentifiers": [{"id": "UK23001120014", "scheme": "uk.gov"}],
                "sireOfficialName": "Camelot",
            }
        ],
    }


@pytest.fixture()
def repro_parturition_payload():
    """Generate a repro parturition payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "isEmbryoImplant": True,
        "damParity": 3,
        "liveProgeny": 2,
        "calvingEase": "EasyAssisted",
    }


@pytest.fixture()
def repro_pregnancy_check_payload():
    """Generate a repro pregnancy check payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "method": "Palpation",
        "result": "Pregnant",
        "foetalAge": 1,
        "foestusCount": 3,
    }


@pytest.fixture()
def attention_payload():
    """Generate a repro status payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "category": "Health",
        "causes": ["Activity", "LyingTooLong"],
        "priority": "Urgent",
    }


@pytest.fixture()
def test_day_result_payload():
    """Generate a test day result event payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "milkWeight24Hours": {"unitCode": "KGM", "value": 20},
        "testDayCode": "Dry",
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
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "traitGroup": "Composite",
        "score": 47,
        "traitScored": "BodyLength",
        "method": "Automated",
    }


@pytest.fixture()
def drying_off_payload(object_id):
    """Generate a drying off payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
    }


@pytest.fixture()
def milking_visit_payload(object_id):
    """Generate a milking visit payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "milkingStartingDateTime": str(datetime.now()),
        "milkingMilkWeight": {"unitCode": "KGM", "value": 10},
    }


@pytest.fixture()
def arrival_payload(object_id):
    """Generate an arrival payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "arrivalReason": "ShowReturn",
        "animalState": {
            "currentLactationParity": 2,
            "lastCalvingDate": str(datetime.now() - timedelta(days=1)),
        },
    }


@pytest.fixture()
def birth_payload(object_id):
    """Generate a birth payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "registrationReason": "Born",
    }


@pytest.fixture()
def death_payload(object_id):
    """Generate a death payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "deathReason": "Age",
    }


@pytest.fixture()
def departure_payload(object_id):
    """Generate an departure payload."""
    return {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "departureReason": "Sale",
        "departureKind": "Sale",
    }


@pytest.fixture()
def machine_payload_updated():
    """Generate an updated machine payload."""
    return {
        "manufacturer": "Generic Machine Ltd.",
        "model": "IronHorse XT-450",
        "type": ["Vehicle", "Tractor"],
    }


@pytest.fixture()
def feed_payload(object_id):
    """Generate an feed payload."""
    return {
        "id": object_id,
        "category": "Roughage",
        "type": {"id": "FC0303", "scheme": "org.fao"},
        "active": True,
    }


@pytest.fixture()
def feed_payload_updated(object_id):
    """Generate an feed payload."""
    return {
        "id": object_id,
        "category": "Additives",
        "name": "LactoMaxx",
        "active": False,
    }


@pytest.fixture()
def feed_storage_payload(object_id):
    """Generate an feed storage payload."""
    return {"id": object_id, "feedId": object_id, "name": "Feed Storage 9000"}


@pytest.fixture()
def feed_storage_payload_updated(object_id):
    """Generate an feed storage payload."""
    return {
        "id": object_id,
        "feedId": object_id,
        "name": "Feed Storage 3000",
        "isActive": False,
    }


@pytest.fixture()
def medicine_payload():
    """Generate an medicine storage payload."""
    return {
        "name": "Betamox LA Injection",
        "approved": "Approved",
    }


@pytest.fixture()
def medicine_payload_updated():
    """Generate an medicine storage payload."""
    return {
        "name": "Betamox LA Injection",
        "approved": "Approved",
        "registeredID": {"id": "6142-50B", "scheme": "uk.gov"},
    }


@pytest.fixture()
def ration_payload(object_id):
    """Generate an ration storage payload."""
    return {"id": {"id": object_id, "scheme": "uk.gov"}, "name": "Super Ration 1000"}


@pytest.fixture()
def ration_payload_updated(object_id):
    """Generate an ration storage payload."""
    return {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "name": "Super Ration 1000",
        "feeds": [
            {"feedId": {"id": object_id, "scheme": "uk.gov"}, "percentage": 10.0}
        ],
        "active": False,
    }
