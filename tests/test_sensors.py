from . import common

ROOT = "measurements"
KEY = "sensors"
PATH = "/" + ROOT + "/" + KEY


class TestSensors:
    def test_create_get_sensor(self, test_client, sensor_payload):
        common.create_get(test_client, PATH, sensor_payload, KEY)

    def test_create_update_sensor(
        self, test_client, sensor_payload, sensor_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, sensor_payload, sensor_payload_updated, KEY
        )

    def test_create_delete_sensor(self, test_client, sensor_payload):
        common.create_delete(test_client, PATH, sensor_payload, KEY)

    def test_get_sensor_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_sensor_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_update_sensor_wrong_payload(
        self, test_client, sensor_payload, sensor_payload_updated
    ):
        sensor_payload_updated["measurement"] = True
        common.create_get_update(
            test_client,
            PATH,
            sensor_payload,
            sensor_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_update_sensor_doesnt_exist(
        self, test_client, object_id, sensor_payload_updated
    ):
        common.update_doesnt_exist(test_client, PATH, sensor_payload_updated, object_id)

    def test_create_duplicate_sensor(self, test_client, sensor_payload):
        common.create_duplicate(test_client, PATH, sensor_payload, KEY)
