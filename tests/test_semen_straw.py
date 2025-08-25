from . import common

ROOT = "objects"
KEY = "semen_straw"
PATH = "/" + ROOT + "/" + KEY


class TestSemenStraw:
    def test_create_get_semen_straw(self, test_client, semen_straw_payload):
        common.create_get(test_client, PATH, semen_straw_payload, KEY)

    def test_create_update_semen_straw(
        self, test_client, semen_straw_payload, semen_straw_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, semen_straw_payload, semen_straw_payload_updated, KEY
        )

    def test_create_delete_semen_straw(self, test_client, semen_straw_payload):
        common.create_delete(test_client, PATH, semen_straw_payload, KEY)

    def test_get_semen_straw_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    # def test_create_semen_straw_wrong_payload(self, test_client):
    #     common.create_wrong_payload(test_client, PATH)

    def test_create_update_semen_straw_wrong_payload(
        self, test_client, semen_straw_payload, semen_straw_payload_updated
    ):
        semen_straw_payload_updated["isSexedSemen"] = 40.6
        common.create_get_update(
            test_client,
            PATH,
            semen_straw_payload,
            semen_straw_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_create_semen_straw_incorrect_enum(self, test_client, semen_straw_payload):
        semen_straw_payload["preservationType"] = "Pickling"
        common.create_get(
            test_client, PATH, semen_straw_payload, KEY, expected_code=422
        )

    def test_update_semen_straw_doesnt_exist(
        self, test_client, object_id, semen_straw_payload_updated
    ):
        common.update_doesnt_exist(
            test_client, PATH, semen_straw_payload_updated, object_id
        )
