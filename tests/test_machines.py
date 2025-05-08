import time
from . import common

ROOT = 'things'
KEY = 'machines'
PATH = '/' + ROOT + '/' + KEY


class TestMachines:
    def test_create_get_machine(self, test_client, machine_payload):
        common.create_get(test_client, PATH,
                          machine_payload, KEY)

    def test_create_update_machine(
            self, test_client, machine_payload, machine_payload_updated):
        common.create_get_update(
            test_client, PATH, machine_payload, machine_payload_updated, KEY)

    def test_create_delete_machine(self, test_client, machine_payload):
        common.create_delete(test_client, PATH,
                             machine_payload, KEY)

    def test_get_machine_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_machine_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_update_machine_wrong_payload(
        self, test_client, machine_payload, machine_payload_updated
    ):
        machine_payload_updated["type"] = True
        common.create_get_update(test_client, PATH, machine_payload,
                                 machine_payload_updated, KEY,
                                 expected_code=422)

    def test_update_machine_doesnt_exist(
        self, test_client, object_id, machine_payload_updated
    ):
        common.update_doesnt_exist(
            test_client, PATH, machine_payload_updated, object_id)
