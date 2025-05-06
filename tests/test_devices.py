import time

class TestDevices:
    def test_create_get_device(self, test_client, device_payload):
        response = test_client.post("/measurements/devices",
                                    json=device_payload)
        response_json = response.json()
        assert response.status_code == 201

        response = test_client.get(
            f"/measurements/devices/?ft={response_json['ft']}")
        assert response.status_code == 200
        assert len(response.json()["devices"]) == 1
        response_json = response.json()["devices"][0]  # TODO: This assumes a single item returned, which also assumes it has been deleted in a later test
        assert response_json["id"] == device_payload["id"]
        assert response_json["softwareVersion"] == device_payload["softwareVersion"]
        assert response_json["serial"] == device_payload["serial"]
        assert response_json["isActive"] == device_payload["isActive"]

    def test_create_update_device(
        self, test_client, device_payload, device_payload_updated
    ):
        response = test_client.post("/measurements/devices/",
                                    json=device_payload)
        response_json = response.json()
        assert response.status_code == 201
        time.sleep(1)
        response = test_client.patch(
            f"/measurements/devices/{response_json['ft']}",
            json=device_payload_updated,
        )
        response_json = response.json()
        assert response.status_code == 202
        assert response_json["id"] == device_payload_updated["id"]
        assert response_json["softwareVersion"] == device_payload_updated["softwareVersion"]
        assert response_json["hardwareVersion"] == device_payload_updated["hardwareVersion"]
        assert response_json["serial"] == device_payload_updated["serial"]
        assert response_json["isActive"] == device_payload_updated["isActive"]

    def test_create_delete_device(self, test_client, device_payload):
        response = test_client.post("/measurements/devices",
                                    json=device_payload)
        response_json = response.json()
        assert response.status_code == 201

        device_id = response_json['ft']

        response = test_client.delete(
            f"/measurements/devices/{device_id}")
        assert response.status_code == 204

        response = test_client.get(
            f"/measurements/devices/?ft={device_id}")
        assert response.status_code == 404

    def test_get_device_not_found(self, test_client, object_id):
        response = test_client.get(
            f"/measurements/devices/?ft={object_id}")
        assert response.status_code == 404

    def test_create_device_wrong_payload(self, test_client):
        response = test_client.post("/measurements/devices/", json={})
        assert response.status_code == 422

    def test_create_update_device_wrong_payload(
        self, test_client, device_payload, device_payload_updated
    ):
        response = test_client.post("/measurements/devices/",
                                    json=device_payload)
        assert response.status_code == 201
        response_json = response.json()
        device_payload_updated["softwareVersion"] = True

        response = test_client.patch(
            f"/measurements/devices/{response_json['ft']}",
            json=device_payload_updated,
        )
        assert response.status_code == 422

    def test_update_device_doesnt_exist(
        self, test_client, object_id, device_payload_updated
    ):
        response = test_client.patch(
            f"/measurements/devices/{object_id}", json=device_payload_updated
        )
        assert response.status_code == 404
