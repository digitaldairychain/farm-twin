from . import common


class TestMedicine:
    def test_create_get_medicine(self, test_client, setup_medicine):
        path, header, key, data = setup_medicine
        common.create_get(test_client, path, header, data, key)

    def test_create_update_medicine(
        self, test_client, setup_medicine, medicine_payload_updated
    ):
        path, header, key, data = setup_medicine
        common.create_get_update(
            test_client, path, header, data, medicine_payload_updated, key
        )

    def test_create_delete_medicine(self, test_client, setup_medicine):
        path, header, key, data = setup_medicine
        common.create_delete(test_client, path, header, data, key)

    def test_get_medicine_not_found(self, test_client, object_id, setup_medicine):
        path, header, _, _ = setup_medicine
        common.get_not_found(test_client, path, header, object_id)

    # def test_create_medicine_wrong_payload(self, test_client):
    #     common.create_wrong_payload(test_client, PATH)

    def test_create_update_medicine_wrong_payload(
        self, test_client, setup_medicine, medicine_payload_updated
    ):
        path, header, key, data = setup_medicine
        medicine_payload_updated["name"] = True
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            medicine_payload_updated,
            key,
            expected_code=422,
        )

    def test_update_medicine_doesnt_exist(
        self, test_client, object_id, medicine_payload_updated, setup_medicine
    ):
        path, header, _, _ = setup_medicine
        common.update_doesnt_exist(
            test_client, path, header, medicine_payload_updated, object_id
        )
