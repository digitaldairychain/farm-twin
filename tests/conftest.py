import os
import random
import string
import uuid
from datetime import datetime, timedelta, timezone
from random import randint

import pytest
from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.main import app

TEST_SOURCE = "{ farm-twin } test"

TEST_USER_USERNAME = "test_user"
TEST_USER_PASSWORD = "".join(
    random.choices(string.ascii_letters + string.digits, k=20)
)

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
    user = {"username": TEST_USER_USERNAME, "password": TEST_USER_PASSWORD}
    yield user


@pytest.fixture()
def fetch_token_user(test_client, setup_user):
    user = setup_user
    user["scope"] = "user"
    yield fetch_header_token(test_client, user)


@pytest.fixture()
def fetch_token_admin(test_client, setup_user):
    user = setup_user
    user["scope"] = "admin"
    yield fetch_header_token(test_client, user)


def fetch_header_token(test_client, user):
    user["grant_type"] = "password"
    response = test_client.post("/users/token", data=user)
    access_token = response.json()["access_token"]
    header = {"Authorization": "Bearer " + access_token}
    return header, response.json(), response.status_code


@pytest.fixture()
def clear_user_in_db():
    client = MongoClient(DB_URL)
    users = client["farm-twin"]["users"]
    delete_operation = {"username": TEST_USER_USERNAME}
    _ = users.delete_one(delete_operation)
    client.close()


@pytest.fixture()
def enable_user_in_db():
    client = MongoClient(DB_URL)
    users = client["farm-twin"]["users"]
    query_filter = {"username": TEST_USER_USERNAME}
    update_operation = {"$set": {"disabled": False}}
    _ = users.update_one(query_filter, update_operation)
    client.close()


@pytest.fixture()
def set_admin_in_db():
    client = MongoClient(DB_URL)
    users = client["farm-twin"]["users"]
    query_filter = {"username": TEST_USER_USERNAME}
    update_operation = {"$set": {"permitted_scopes": ["admin"], "admin": True}}
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
def setup_animal(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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
def setup_location(test_client, fetch_token_admin):
    """Generate a location payload."""
    key = "location"
    path = "/objects/" + key
    data = {
        "identifier": {"id": "UK54321", "scheme": "uk.gov"},
        "name": "Nowhere Farm",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def location_data_updated():
    """Generate an updated location payload."""
    return {
        "identifier": {"id": "UK54321", "scheme": "uk.gov"},
        "name": "Somewhere Farm",
        "timeZoneId": "Europe/Paris",
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_device(test_client, serial, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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
def setup_weight(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_group_weight(test_client, object_id, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_feed_intake(test_client, fetch_token_admin):
    """Generate a feed intake event payload."""
    key = "feed_intake"
    path = "/events/feeding/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "feedingStartingDateTime": datetime.now(timezone.utc).isoformat(),
        "feedVisitDuration": {"unitCode": "MIN", "value": 10},
        "consumedFeed": [
            {
                "feedId": {"id": "test", "scheme": "ft.org"},
                "dryMatterPercentage": 10,
            }
        ],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_withdrawal(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_carcass(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_health_status(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_lactation_status(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_position(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_status(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_abortion(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_do_not_breed(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_heat(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_insemination(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_mating_recommendation(test_client, fetch_token_admin):
    """Generate a repro mating recommendation payload."""
    key = "repro_mating_recommendation"
    path = "/events/reproduction/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "sireRecommendations": [
            {
                "recommendationType": "SireRecommended",
                "sireIdentifiers": [
                    {"id": "UK23001120014", "scheme": "uk.gov"}
                ],
                "sireOfficialName": "Camelot",
            }
        ],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_parturition(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_repro_pregnancy_check(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_attention(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_test_day_result(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_sensor(test_client, object_id, fetch_token_admin):
    """Generate a sensor payload."""
    key = "sensors"
    path = "/measurements/" + key
    data = {
        "device": object_id,
        "measurement": "Air Temperature",
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


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
def setup_sample(test_client, object_id, fetch_token_admin):
    """Generate a sample payload."""
    key = "samples"
    path = "/measurements/" + key
    data = {
        "sensor": object_id,
        "timestamp": str(datetime.now()),
        "value": float(randint(10000, 99999)),
        "predicted": False,
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_image(test_client, object_id, fetch_token_admin):
    """Generate an earth observation image metadata payload."""
    key = "images"
    path = "/measurements/" + key
    data = {
        "platform": "Sentinel-2A",
        "instrument": "MSI",
        "timestamp": str(datetime.now()),
        "uri": "https://example.com/eo/sentinel2-20250101.tif",
        "resolution": 10.0,
        "cloudCover": 5.2,
        "bands": ["B02", "B03", "B04", "B08"],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def image_payload_updated(object_id):
    """Generate an updated earth observation image metadata payload."""
    return {
        "platform": "Landsat-8",
        "instrument": "OLI",
        "uri": "https://example.com/eo/landsat8-20250201.tif",
        "resolution": 30.0,
        "cloudCover": 12.5,
        "bands": ["B1", "B2", "B3", "B4", "B5"],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_machine(test_client, fetch_token_admin):
    """Generate a conformation payload."""
    key = "machines"
    path = "/objects/" + key
    data = {
        "manufacturer": "Acme Machine Co.",
        "model": "Machine 3000",
        "type": ["Vehicle", "Off-Road", "Utility"],
        "registration": "BD51 SMR",
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def machine_payload_updated():
    """Generate an updated machine payload."""
    return {
        "manufacturer": "Generic Machine Ltd.",
        "model": "IronHorse XT-450",
        "type": ["Vehicle", "Tractor"],
    }


@pytest.fixture()
def setup_conformation(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_drying_off(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_milking_visit(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_arrival(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_birth(object_id, test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_death(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_departure(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_feed(object_id, test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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
def setup_feed_storage(object_id, test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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
def setup_medicine(test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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
def setup_ration(object_id, test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def ration_payload_updated(object_id):
    """Generate an ration storage payload."""
    return {
        "id": {"id": object_id, "scheme": "uk.gov"},
        "name": "Super Ration 1000",
        "feeds": [
            {
                "feedId": {"id": object_id, "scheme": "uk.gov"},
                "percentage": 10.0,
            }
        ],
        "active": False,
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now()),
        },
    }


@pytest.fixture()
def setup_embryo(object_id, test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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
def setup_semen_straw(object_id, test_client, fetch_token_admin):
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
    header, _, _ = fetch_token_admin
    yield path, header, key, data
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


@pytest.fixture()
def setup_treatment(object_id, test_client, fetch_token_admin):
    """Generate a treatment payload."""
    key = "treatment"
    path = "/events/health/" + key
    data = {
        "medicine": {
            "identifier": {
                "id": object_id,
                "scheme": "uk.gov"
            },
            "family": "Veterinary Supplies",
            "name": "Metacam"
        },
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "procedure": "Oral",
        "batches": [
            {
                "identifier": "00201",
                "expiryDate": str(datetime.now() + timedelta(days=1))
            }
        ],
        "withdrawals": [
            {
                "productType": "Meat",
                "endDate": str(datetime.now() + timedelta(days=1))
            }
        ],
        "dose": {
            "doseQuantity": 3.5,
            "doseUnits": "MLT"
        },
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now())
        }
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)


@pytest.fixture()
def setup_diagnosis(test_client, fetch_token_admin):
    """Generate a diagnosis payload."""
    key = "diagnosis"
    path = "/events/health/" + key
    data = {
        "animal": {"id": "UK230011200123", "scheme": "uk.gov"},
        "diagnoses": [
            {
                "id": "DEF0101",
                "name": "Mastitis",
                "stage": "Early",
                "severity": "Light",
                "severityScore": 10,
                "positions": [
                    {
                        "position": "UdderFrontLeft"
                    },
                    {
                        "position": "UdderFrontRight"
                    }
                ]
            }
        ],
        "meta": {
            "source": TEST_SOURCE,
            "sourceId": str(uuid.uuid4()),
            "modified": str(datetime.now())
        }
    }
    header, _, _ = fetch_token_admin
    yield path, header, key, data
    clear_test_data(test_client, path, key)
