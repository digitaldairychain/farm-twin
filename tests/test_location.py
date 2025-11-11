from . import common


class TestLocation:
    def test_create_get_location(self, test_client, setup_location):
        path, header, key, data = setup_location
        common.create_get(test_client, path, header, data, key)

    def test_create_update_location(self, test_client, setup_location, location_data_updated):
        path, header, key, data = setup_location
        common.create_get_update(
            test_client, path, header, data, location_data_updated, key
        )

    def test_create_delete_location(self, test_client, setup_location):
        path, header, key, data = setup_location
        common.create_delete(test_client, path, header, data, key)

    def test_get_location_not_found(self, test_client, setup_location, object_id):
        path, header, _, _ = setup_location
        common.get_not_found(test_client, path, header, object_id)

    def test_create_location_wrong_payload(self, test_client, setup_location):
        path, header, _, _ = setup_location
        common.create_wrong_payload(test_client, path, header)

    def test_create_update_location_wrong_payload(
        self, test_client, setup_location, location_data_updated
    ):
        path, header, key, data = setup_location
        location_data_updated["timeZoneId"] = False
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            location_data_updated,
            key,
            expected_code=422,
        )

    def test_update_location_doesnt_exist(
        self, test_client, object_id, setup_location, location_data_updated
    ):
        path, header, _, _ = setup_location
        common.update_doesnt_exist(
            test_client, path, header, location_data_updated, object_id
        )
