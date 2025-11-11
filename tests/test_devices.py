from . import common

ROOT = "objects"
KEY = "devices"
PATH = "/" + ROOT + "/" + KEY


class TestDevices:
    def test_create_get_device(self, test_client, setup_device):
        path, header, key, data = setup_device
        common.create_get(test_client, path, header, data, key)

    def test_create_update_device(
        self, test_client, setup_device, device_data_updated
    ):
        path, header, key, data = setup_device
        common.create_get_update(
            test_client, path, header, data, device_data_updated, key
        )

    def test_create_delete_device(self, test_client, setup_device):
        path, header, key, data = setup_device
        common.create_delete(test_client, path, header, data, key)

    def test_get_device_not_found(self, test_client, setup_device, object_id):
        path, header, _, _ = setup_device
        common.get_not_found(test_client, path, header, object_id)

    def test_create_device_wrong_payload(self, test_client, setup_device):
        path, header, _, _ = setup_device
        common.create_wrong_payload(test_client, path, header)

    def test_create_update_device_wrong_payload(
        self, test_client, setup_device, device_data_updated
    ):
        path, header, key, data = setup_device
        device_data_updated["softwareVersion"] = True
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            device_data_updated,
            key,
            expected_code=422,
        )

    def test_create_device_incorrect_enum(self, test_client, setup_device):
        path, header, key, data = setup_device
        data["supportedMessages"] = "TCP/IP"
        common.create_get(
            test_client, path, header, data, key, expected_code=422
        )

    def test_update_device_doesnt_exist(
        self, test_client, object_id, device_data_updated, setup_device
    ):
        path, header, _, _ = setup_device
        common.update_doesnt_exist(
            test_client, path, header, device_data_updated, object_id
        )

    def test_create_duplicate_device(self, test_client, setup_device):
        path, header, key, data = setup_device
        common.create_duplicate(test_client, path, header, data, key)
