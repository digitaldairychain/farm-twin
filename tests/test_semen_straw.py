from . import common


class TestSemenStraw:
    def test_create_get_semen_straw(self, test_client, setup_semen_straw):
        path, key, data = setup_semen_straw
        common.create_get(test_client, path, data, key)

    def test_create_update_semen_straw(
        self, test_client, setup_semen_straw, semen_straw_payload_updated
    ):
        path, key, data = setup_semen_straw
        common.create_get_update(
            test_client, path, data, semen_straw_payload_updated, key
        )

    def test_create_delete_semen_straw(self, test_client, setup_semen_straw):
        path, key, data = setup_semen_straw
        common.create_delete(test_client, path, data, key)

    def test_get_semen_straw_not_found(self, test_client, object_id, setup_semen_straw):
        path, _, _ = setup_semen_straw
        common.get_not_found(test_client, path, object_id)

    # def test_create_semen_straw_wrong_payload(self, test_client):
    #     common.create_wrong_payload(test_client, PATH)

    def test_create_update_semen_straw_wrong_payload(
        self, test_client, setup_semen_straw, semen_straw_payload_updated
    ):
        path, key, data = setup_semen_straw
        semen_straw_payload_updated["isSexedSemen"] = 40.6
        common.create_get_update(
            test_client,
            path,
            data,
            semen_straw_payload_updated,
            key,
            expected_code=422,
        )

    def test_create_semen_straw_incorrect_enum(self, test_client, setup_semen_straw):
        path, key, data = setup_semen_straw
        data["preservationType"] = "Pickling"
        common.create_get(test_client, path, data, key, expected_code=422)

    def test_update_semen_straw_doesnt_exist(
        self, test_client, object_id, semen_straw_payload_updated, setup_semen_straw
    ):
        path, _, _ = setup_semen_straw
        common.update_doesnt_exist(
            test_client, path, semen_straw_payload_updated, object_id
        )
