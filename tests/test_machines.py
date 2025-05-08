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
        self, test_client, machine_payload, machine_payload_updated,
        check_object_similarity
    ):
        response = test_client.post("/things/machines/",
                                    json=machine_payload)
        response_json = response.json()
        assert response.status_code == 201
        check_object_similarity(machine_payload, response_json)
        time.sleep(1)
        response = test_client.patch(
            f"/things/machines/{response_json['ft']}",
            json=machine_payload_updated,
        )
        response_json = response.json()
        assert response.status_code == 202
        check_object_similarity(machine_payload_updated, response_json)

    def test_create_delete_machine(self, test_client, machine_payload):
        response = test_client.post("/things/machines",
                                    json=machine_payload)
        response_json = response.json()
        assert response.status_code == 201

        machine_id = response_json['ft']

        response = test_client.delete(
            f"/things/machines/{machine_id}")
        assert response.status_code == 204

        response = test_client.get(
            f"/things/machines/?ft={machine_id}")
        assert response.status_code == 404

    def test_get_machine_not_found(self, test_client, object_id):
        response = test_client.get(
            f"/things/machines/?ft={object_id}")
        assert response.status_code == 404

    def test_create_machine_wrong_payload(self, test_client):
        response = test_client.post("/things/machines/", json={})
        assert response.status_code == 422

    def test_create_update_machine_wrong_payload(
        self, test_client, machine_payload, machine_payload_updated
    ):
        response = test_client.post("/things/machines/",
                                    json=machine_payload)
        assert response.status_code == 201
        response_json = response.json()
        machine_payload_updated["type"] = True

        response = test_client.patch(
            f"/things/machines/{response_json['ft']}",
            json=machine_payload_updated,
        )
        assert response.status_code == 422

    def test_update_machine_doesnt_exist(
        self, test_client, object_id, machine_payload_updated
    ):
        response = test_client.patch(
            f"/things/machines/{object_id}", json=machine_payload_updated
        )
        assert response.status_code == 404
