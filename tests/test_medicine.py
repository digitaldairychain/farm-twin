from . import common

ROOT = "things"
KEY = "medicine"
PATH = "/" + ROOT + "/" + KEY


class TestAnimals:
    def test_create_get_medicine(self, test_client, medicine_payload):
        common.create_get(test_client, PATH, medicine_payload, KEY)

    def test_create_update_medicine(
        self, test_client, medicine_payload, medicine_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, medicine_payload, medicine_payload_updated, KEY
        )

    def test_create_delete_medicine(self, test_client, medicine_payload):
        common.create_delete(test_client, PATH, medicine_payload, KEY)

    def test_get_medicine_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    # def test_create_medicine_wrong_payload(self, test_client):
    #     common.create_wrong_payload(test_client, PATH)

    def test_create_update_medicine_wrong_payload(
        self, test_client, medicine_payload, medicine_payload_updated
    ):
        medicine_payload_updated["name"] = True
        common.create_get_update(
            test_client,
            PATH,
            medicine_payload,
            medicine_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_update_medicine_doesnt_exist(
        self, test_client, object_id, medicine_payload_updated
    ):
        common.update_doesnt_exist(
            test_client, PATH, medicine_payload_updated, object_id
        )
