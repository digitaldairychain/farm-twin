from . import common

ROOT = "things"
KEY = "ration"
PATH = "/" + ROOT + "/" + KEY


class TestRation:
    def test_create_get_ration(self, test_client, ration_payload):
        common.create_get(test_client, PATH, ration_payload, KEY)

    def test_create_update_ration(
        self, test_client, ration_payload, ration_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, ration_payload, ration_payload_updated, KEY
        )

    def test_create_delete_ration(self, test_client, ration_payload):
        common.create_delete(test_client, PATH, ration_payload, KEY)

    def test_get_ration_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_ration_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_update_ration_wrong_payload(
        self, test_client, ration_payload, ration_payload_updated
    ):
        ration_payload_updated["active"] = 9.76
        common.create_get_update(
            test_client,
            PATH,
            ration_payload,
            ration_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_update_ration_doesnt_exist(
        self, test_client, object_id, ration_payload_updated
    ):
        common.update_doesnt_exist(test_client, PATH, ration_payload_updated, object_id)
