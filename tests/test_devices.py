from . import common

ROOT = "objects"
KEY = "devices"
PATH = "/" + ROOT + "/" + KEY


class TestDevices:
    def test_create_get_device(self, test_client, device_payload):
        common.create_get(test_client, PATH, device_payload, KEY)

    def test_create_update_device(
        self, test_client, device_payload, device_payload_updated
    ):
        common.create_get_update(
            test_client, PATH, device_payload, device_payload_updated, KEY
        )

    def test_create_delete_device(self, test_client, device_payload):
        common.create_delete(test_client, PATH, device_payload, KEY)

    def test_get_device_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_device_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_update_device_wrong_payload(
        self, test_client, device_payload, device_payload_updated
    ):
        device_payload_updated["softwareVersion"] = True
        common.create_get_update(
            test_client,
            PATH,
            device_payload,
            device_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_create_device_incorrect_enum(self, test_client, device_payload):
        device_payload["supportedMessages"] = "TCP/IP"
        common.create_get(test_client, PATH, device_payload, KEY, expected_code=422)

    def test_update_device_doesnt_exist(
        self, test_client, object_id, device_payload_updated
    ):
        common.update_doesnt_exist(test_client, PATH, device_payload_updated, object_id)

    def test_create_duplicate_device(self, test_client, device_payload):
        common.create_duplicate(test_client, PATH, device_payload, KEY)
