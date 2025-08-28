from . import common


class TestRation:
    def test_create_get_ration(self, test_client, setup_ration):
        path, key, data = setup_ration
        common.create_get(test_client, path, data, key)

    def test_create_update_ration(
        self, test_client, setup_ration, ration_payload_updated
    ):
        path, key, data = setup_ration
        common.create_get_update(
            test_client, path, data, ration_payload_updated, key
        )

    def test_create_delete_ration(self, test_client, setup_ration):
        path, key, data = setup_ration
        common.create_delete(test_client, path, data, key)

    def test_get_ration_not_found(self, test_client, object_id, setup_ration):
        path, _, _ = setup_ration
        common.get_not_found(test_client, path, object_id)

    def test_create_ration_wrong_payload(self, test_client, setup_ration):
        path, _, _ = setup_ration
        common.create_wrong_payload(test_client, path)

    def test_create_update_ration_wrong_payload(
        self, test_client, setup_ration, ration_payload_updated
    ):
        path, key, data = setup_ration
        ration_payload_updated["active"] = 9.76
        common.create_get_update(
            test_client,
            path,
            data,
            ration_payload_updated,
            key,
            expected_code=422,
        )

    def test_update_ration_doesnt_exist(
        self, test_client, object_id, setup_ration, ration_payload_updated
    ):
        path, _, _ = setup_ration
        common.update_doesnt_exist(
            test_client, path, ration_payload_updated, object_id)
