import uuid
import os
from datetime import datetime, timedelta, timezone
from random import randint
from dotenv import load_dotenv

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.main import app

TEST_SOURCE = "{ farm-twin } test"

load_dotenv()
DB_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
DB_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
DB_URL = f"mongodb://{DB_USER}:{DB_PASS}@localhost"


@pytest.fixture()
def test_client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def object_id():
    """Generate a random uuid."""
    return str(ObjectId())


@pytest.fixture()
def serial():
    """Generate a random serial number."""
    return str(randint(10000, 99999))


@pytest.fixture
def setup_registration(setup_user):
    registration = {
        "email": "test@test.com",
        "full_name": "Test User",
    }
    yield registration | setup_user


@pytest.fixture
def setup_user():
    """Generate a user payload."""
    user = {
        "username": "test_user",
        "password": "H:=MF70v<tm9"
    }
    yield user


@pytest.fixture()
def fetch_token(test_client, setup_user):
    user = setup_user
    user["scope"] = "user"
    user["grant_type"] = "password"
    response = test_client.post('/users/token', data=user)
    yield response


@pytest.fixture()
def enable_user_in_db():
    client = MongoClient(DB_URL)
    users = client["farm-twin"]["users"]
    query_filter = {'username': 'test_user'}
    update_operation = {'$set':
                        {'disabled': False}
                        }
    _ = users.update_one(query_filter, update_operation)
    client.close()


def clear_test_data(test_client, path, key) -> None:
    response = test_client.get(path + f"/?source={TEST_SOURCE}")
    if response.status_code == 200:
        for item in response.json()[key]:
            _id = item["ft"]
            test_client.delete(f"{path}/{_id}")
        response = test_client.get(path + f"/?source={TEST_SOURCE}")
        assert response.status_code == 404


@pytest.fixture()
def setup_animal(test_client):
    """Generate an animal payload."""
    key = "animals"
    path = "/objects/" + key
    data = {
        "identifier": {"id": "UK230011200123", "scheme": "uk.gov"},
        "specie": "Cattle",
        "gender": "Female",
        "birthDate": "2025-04-24 12:18:06.625573",
        "productionPurpose": "Milk",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "Healthy",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def animal_data_updated():
    """Generate an updated animal payload."""
    return {
        "identifier": {"id": "UK230011200124", "scheme": "uk.gov"},
        "specie": "Cattle",
        "gender": "Male",
        "productionPurpose": "Wool",
        "status": "Alive",
        "reproductionStatus": "Open",
        "lactationStatus": "Fresh",
        "healthStatus": "InTreatment",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_device(test_client, serial):
    """Generate an animal payload."""
    key = "devices"
    path = "/objects/" + key
    data = {
        "id": "Sample",
        "serial": serial,
        "softwareVersion": "1.3",
        "manufacturer": {
            "id": "Acme Sensor Co.",
        },
        "isActive": True,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def device_data_updated(serial):
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
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_weight(test_client):
    """Generate a weight event payload."""
    key = "weight"
    path = "/events/performance/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "weight": {
            "measurement": float(randint(453, 816)),
            "units": "KGM",
            "method": "LoadCell",
            "resolution": float(randint(1, 9) / 10),
        },
        "device": {"manufacturerName": "Acme Sensor Co."},
        "timeOffFeed": float(randint(1, 5)),
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_group_weight(test_client, object_id):
    """Generate a group weight event payload."""
    key = "group_weight"
    path = "/events/performance/" + key
    data = {
        "groupMethod": "EmbeddedAnimalSet",
        "embeddedAnimalSet": {
            "id": object_id,
            "member": [{"id": "UK230011200123", "scheme": "uk.gov"}],
            "meta": {
                "source": TEST_SOURCE,
                "sourceId": str(uuid.uuid4()),
                "modified": str(datetime.now()),
            },
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
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_feed_intake(test_client):
    """Generate a feed intake event payload."""
    key = "feed_intake"
    path = "/events/feeding/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "feedingStartingDateTime": datetime.now(timezone.utc).isoformat(),
        "feedVisitDuration": {"unitCode": "MIN", "value": 10},
        "consumedFeed": [
            {"feedId": {"id": "test", "scheme": "ft.org"}, "dryMatterPercentage": 10}
        ],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_withdrawal(test_client):
    """Generate a withdrawal payload."""
    key = "withdrawal"
    path = "/events/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "endDateTime": datetime.now(timezone.utc).isoformat(),
        "productType": "Eggs",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_carcass(test_client):
    """Generate a withdrawal payload."""
    key = "carcass"
    path = "/events/observations/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "side": "Left",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_health_status(test_client):
    """Generate a health status payload."""
    key = "health_status"
    path = "/events/observations/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "observedStatus": "Healthy",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_lactation_status(test_client):
    """Generate a lactation status payload."""
    key = "lactation_status"
    path = "/events/milking/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "observedStatus": "Fresh",
        "eventDateTime": datetime.now(timezone.utc).isoformat(),
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_position(test_client):
    """Generate a position payload."""
    key = "position"
    path = "/events/observations/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "positionName": "Yard",
        "eventDateTime": datetime.now(timezone.utc).isoformat(),
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_status(test_client):
    """Generate a repro status payload."""
    key = "repro_status"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "observedStatus": "Pregnant",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_abortion(test_client):
    """Generate a repro abortion payload."""
    key = "repro_abortion"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_do_not_breed(test_client):
    """Generate a repro do not breed payload."""
    key = "repro_do_not_breed"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "doNotBreed": True,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_heat(test_client):
    """Generate a repro heat payload."""
    key = "repro_heat"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "heatDetectionMethod": "Visual",
        "certainty": "Suspect",
        "commencementDateTime": str(datetime.now() - timedelta(days=1)),
        "expirationDateTime": str(datetime.now() + timedelta(days=1)),
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_insemination(test_client):
    """Generate a repro insemination payload."""
    key = "repro_insemination"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "inseminationType": "NaturalService",
        "sireOfficialName": "Frankel",
        "eventDateTime": str(datetime.now()),
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_mating_recommendation(test_client):
    """Generate a repro mating recommendation payload."""
    key = "repro_mating_recommendation"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "sireRecommendations": [
            {
                "recommendationType": "SireRecommended",
                "sireIdentifiers": [{"id": "UK23001120014", "scheme": "uk.gov"}],
                "sireOfficialName": "Camelot",
            }
        ],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_parturition(test_client):
    """Generate a repro parturition payload."""
    key = "repro_parturition"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "isEmbryoImplant": True,
        "damParity": 3,
        "liveProgeny": 2,
        "calvingEase": "EasyAssisted",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_pregnancy_check(test_client):
    """Generate a repro pregnancy check payload."""
    key = "repro_pregnancy_check"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "method": "Palpation",
        "result": "Pregnant",
        "foetalAge": 1,
        "foestusCount": 3,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_attention(test_client):
    """Generate an attention payload."""
    key = "attention"
    path = "/events/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "category": "Health",
        "causes": ["Activity", "LyingTooLong"],
        "priority": "Urgent",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_test_day_result(test_client):
    """Generate a test day result event payload."""
    key = "test_day_result"
    path = "/events/milking/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "milkWeight24Hours": {"unitCode": "KGM", "value": 20},
        "testDayCode": "Dry",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def sensor_payload(object_id, serial):
    """Generate a sensor payload."""
    return {
        "device": object_id,
        "measurement": "Air Temperature",
    }


@pytest.fixture()
def sensor_payload_updated(
    object_id,
    serial,
):
    """Generate an updated sensor payload."""
    return {
        "device": object_id,
        "serial": serial,
        "measurement": "Soil Temperature",
    }


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
def machine_payload_updated():
    """Generate an updated machine payload."""
    return {
        "manufacturer": "Generic Machine Ltd.",
        "model": "IronHorse XT-450",
        "type": ["Vehicle", "Tractor"],
    }


@pytest.fixture()
def setup_conformation(test_client):
    """Generate a conformation payload."""
    key = "conformation"
    path = "/events/performance/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "traitGroup": "Composite",
        "score": 47,
        "traitScored": "BodyLength",
        "method": "Automated",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_drying_off(test_client):
    """Generate a drying off payload."""
    key = "drying_off"
    path = "/events/milking/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_milking_visit(test_client):
    """Generate a milking visit payload."""
    key = "visit"
    path = "/events/milking/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "milkingStartingDateTime": str(datetime.now()),
        "milkingMilkWeight": {"unitCode": "KGM", "value": 10},
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_arrival(test_client):
    """Generate an arrival payload."""
    key = "arrival"
    path = "/events/movement/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "arrivalReason": "ShowReturn",
        "animalState": {
            "currentLactationParity": 2,
            "lastCalvingDate": str(datetime.now() - timedelta(days=1)),
        },
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_birth(object_id, test_client):
    """Generate a birth payload."""
    key = "birth"
    path = "/events/movement/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "registrationReason": "Born",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_death(test_client):
    """Generate a death payload."""
    key = "death"
    path = "/events/movement/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "deathReason": "Age",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_departure(test_client):
    """Generate an departure payload."""
    key = "departure"
    path = "/events/movement/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "departureReason": "Sale",
        "departureKind": "Sale",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_feed(object_id, test_client):
    """Generate an feed payload."""
    key = "feed"
    path = "/objects/" + key
    data = {
        "id": object_id,
        "category": "Roughage",
        "type": {"id": "FC0303", "scheme": "org.fao"},
        "active": True,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def feed_payload_updated(object_id):
    """Generate an feed payload."""
    return {
        "id": object_id,
        "category": "Additives",
        "name": "LactoMaxx",
        "active": False,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_feed_storage(object_id, test_client):
    """Generate an feed storage payload."""
    key = "feed_storage"
    path = "/objects/" + key
    data = {
        "id": object_id,
        "feedId": object_id,
        "name": "Feed Storage 9000",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def feed_storage_payload_updated(object_id):
    """Generate an feed storage payload."""
    return {
        "id": object_id,
        "feedId": object_id,
        "name": "Feed Storage 3000",
        "isActive": False,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_medicine(test_client):
    """Generate an medicine storage payload."""
    key = "medicine"
    path = "/objects/" + key
    data = {
        "name": "Betamox LA Injection",
        "approved": "Approved",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def medicine_payload_updated():
    """Generate an medicine storage payload."""
    return {
        "name": "Betamox LA Injection",
        "approved": "Approved",
        "registeredID": {"id": "6142-50B", "scheme": "uk.gov"},
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_ration(object_id, test_client):
    """Generate an ration storage payload."""
    key = "ration"
    path = "/objects/" + key
    data = {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "name": "Super Ration 1000",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


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
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_embryo(object_id, test_client):
    """Generate an embryo payload."""
    key = "embryo"
    path = "/objects/" + key
    data = {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "dateCollected": str(datetime.now()),
        "donorURI": object_id,
        "sireOfficialName": "Frankenstein",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def embryo_data_updated(object_id):
    """Generate an embryo payload."""
    return {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "sireURI": object_id,
        "donorIdentifiers": [
            {"id": object_id, "scheme": "uk.gov"},
            {"id": object_id, "scheme": "uk.gov"},
        ],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_semen_straw(object_id, test_client):
    """Generate an semen straw payload."""
    key = "semen_straw"
    path = "/objects/" + key
    data = {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "collectionCentre": "London, UK",
        "dateCollected": str(datetime.now()),
        "sireURI": object_id,
        "preservationType": "Liquid",
        "isSexedSemen": True,
        "sexedGender": "Male",
        "sexedPercentage": 95,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    yield path, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def semen_straw_payload_updated(object_id):
    """Generate an semen straw payload."""
    return {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "sireOfficialName": "Spongebob",
        "sireIdentifiers": [
            {"id": object_id, "scheme": "uk.gov"},
            {"id": object_id, "scheme": "uk.gov"},
        ],
        "preservationType": "Frozen",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
