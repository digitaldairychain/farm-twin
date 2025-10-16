from . import common

ROOT = "objects"
KEY = "embryo"
PATH = "/" + ROOT + "/" + KEY


class TestEmbryo:
    def test_create_get_embryo(self, test_client, setup_embryo):
        path, key, data = setup_embryo
        common.create_get(test_client, path, data, key)

    def test_create_update_embryo(self, test_client, setup_embryo, embryo_data_updated):
        path, key, data = setup_embryo
        common.create_get_update(test_client, path, data, embryo_data_updated, key)

    def test_create_delete_embryo(self, test_client, setup_embryo):
        path, key, data = setup_embryo
        common.create_delete(test_client, path, data, key)

    def test_get_embryo_not_found(self, test_client, object_id, setup_embryo):
        path, _, _ = setup_embryo
        common.get_not_found(test_client, path, object_id)

    # def test_create_embryo_wrong_payload(self, test_client):
    #     common.create_wrong_payload(test_client, PATH)

    def test_create_update_embryo_wrong_payload(
        self, test_client, setup_embryo, embryo_data_updated
    ):
        path, key, data = setup_embryo
        embryo_data_updated["sireURI"] = 9.76
        common.create_get_update(
            test_client,
            path,
            data,
            embryo_data_updated,
            key,
            expected_code=422,
        )

    def test_update_embryo_doesnt_exist(
        self, test_client, object_id, setup_embryo, embryo_data_updated
    ):
        path, _, _ = setup_embryo
        common.update_doesnt_exist(test_client, path, embryo_data_updated, object_id)
