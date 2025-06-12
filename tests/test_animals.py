from . import common

ROOT = "things"
KEY = "animals"
PATH = "/" + ROOT + "/" + KEY


class TestAnimals:
    def test_create_get_animal(self, test_client, animal_payload):
        common.create_get(test_client, PATH, animal_payload, KEY)

    def test_create_update_animal(
        self, test_client, animal_payload, animal_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, animal_payload, animal_payload_updated, KEY
        )

    def test_create_delete_animal(self, test_client, animal_payload):
        common.create_delete(test_client, PATH, animal_payload, KEY)

    def test_get_animal_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_animal_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_update_animal_wrong_payload(
        self, test_client, animal_payload, animal_payload_updated
    ):
        animal_payload_updated["gender"] = True
        common.create_get_update(
            test_client,
            PATH,
            animal_payload,
            animal_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_create_animal_incorrect_enum(self, test_client, animal_payload):
        animal_payload["productionPurpose"] = "Astronaut"
        common.create_get(test_client, PATH, animal_payload, KEY, expected_code=422)

    def test_update_animal_doesnt_exist(
        self, test_client, object_id, animal_payload_updated
    ):
        common.update_doesnt_exist(test_client, PATH, animal_payload_updated, object_id)
