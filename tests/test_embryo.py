from . import common

ROOT = "things"
KEY = "embryo"
PATH = "/" + ROOT + "/" + KEY


class TestSemenStraw:
    def test_create_get_embryo(self, test_client, embryo_payload):
        common.create_get(test_client, PATH, embryo_payload, KEY)

    def test_create_update_embryo(
        self, test_client, embryo_payload, embryo_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, embryo_payload, embryo_payload_updated, KEY
        )

    def test_create_delete_embryo(self, test_client, embryo_payload):
        common.create_delete(test_client, PATH, embryo_payload, KEY)

    def test_get_embryo_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    # def test_create_embryo_wrong_payload(self, test_client):
    #     common.create_wrong_payload(test_client, PATH)

    def test_create_update_embryo_wrong_payload(
        self, test_client, embryo_payload, embryo_payload_updated
    ):
        embryo_payload_updated["sireURI"] = 9.76
        common.create_get_update(
            test_client,
            PATH,
            embryo_payload,
            embryo_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_update_embryo_doesnt_exist(
        self, test_client, object_id, embryo_payload_updated
    ):
        common.update_doesnt_exist(test_client, PATH, embryo_payload_updated, object_id)
