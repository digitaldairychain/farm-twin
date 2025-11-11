from . import common


class TestSensors:
    def test_create_get_sensor(self, test_client, setup_sensor):
        path, header, key, data = setup_sensor
        common.create_get(test_client, path, header, data, key)

    def test_create_update_sensor(
        self, test_client, setup_sensor, sensor_payload_updated
    ):
        path, header, key, data = setup_sensor
        common.create_get_update(
            test_client, path, header, data, sensor_payload_updated, key
        )

    def test_create_delete_sensor(self, test_client, setup_sensor):
        path, header, key, data = setup_sensor
        common.create_delete(test_client, path, header, data, key)

    def test_get_sensor_not_found(self, test_client, object_id, setup_sensor):
        path, header, _, _ = setup_sensor
        common.get_not_found(test_client, path, header, object_id)

    def test_create_sensor_wrong_payload(self, test_client, setup_sensor):
        path, header, _, _ = setup_sensor
        common.create_wrong_payload(test_client, path, header)

    def test_create_update_sensor_wrong_payload(
        self, test_client, setup_sensor, sensor_payload_updated
    ):
        path, header, key, data = setup_sensor
        sensor_payload_updated["measurement"] = True
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            sensor_payload_updated,
            key,
            expected_code=422,
        )

    def test_create_sensor_incorrect_enum(self, test_client, setup_sensor):
        path, header, key, data = setup_sensor
        data["category"] = "BreakfastCereal"
        common.create_get(
            test_client, path, header, data, key, expected_code=422
        )

    def test_update_sensor_doesnt_exist(
        self, test_client, object_id, sensor_payload_updated, setup_sensor
    ):
        path, header, _, _ = setup_sensor
        common.update_doesnt_exist(
            test_client, path, header, sensor_payload_updated, object_id
        )
