from . import common


class TestMachines:
    def test_create_get_machine(self, test_client, setup_machine):
        path, header, key, data = setup_machine
        common.create_get(test_client, path, header, data, key)

    def test_create_update_machine(
        self, test_client, setup_machine, machine_payload_updated
    ):
        path, header, key, data = setup_machine
        common.create_get_update(
            test_client, path, header, data, machine_payload_updated, key
        )

    def test_create_delete_machine(self, test_client, setup_machine):
        path, header, key, data = setup_machine
        common.create_delete(test_client, path, header, data, key)

    def test_get_machine_not_found(self, test_client, object_id, setup_machine):
        path, header, _, _ = setup_machine
        common.get_not_found(test_client, path, header, object_id)

    def test_create_machine_wrong_payload(self, test_client, setup_machine):
        path, header, _, _ = setup_machine
        common.create_wrong_payload(test_client, path, header)

    def test_create_update_machine_wrong_payload(
        self, test_client, setup_machine, machine_payload_updated
    ):
        path, header, key, data = setup_machine
        machine_payload_updated["type"] = True
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            machine_payload_updated,
            key,
            expected_code=422,
        )

    def test_update_machine_doesnt_exist(
        self, test_client, object_id, machine_payload_updated, setup_machine
    ):
        path, header, _, _ = setup_machine
        common.update_doesnt_exist(
            test_client, path, header, machine_payload_updated, object_id
        )
