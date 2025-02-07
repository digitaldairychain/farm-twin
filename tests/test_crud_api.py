def test_liveliness(test_client):
    response = test_client.get("/version/")
    assert response.status_code == 200


class TestDevices:
    def test_create_get_device(self, test_client, device_payload):
        response = test_client.post("/measurements/devices",
                                    json=device_payload)
        response_json = response.json()
        assert response.status_code == 201

        response = test_client.get(
            f"/measurements/devices/{device_payload['tag']}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["tag"] == device_payload["tag"]
        assert response_json["vendor"] == "Acme Sensor Co."
        assert response_json["model"] == "Super Device 9000"

    def test_create_update_device(
        self, test_client, device_payload, device_payload_updated
    ):
        response = test_client.post("/measurements/devices/",
                                    json=device_payload)
        response_json = response.json()
        assert response.status_code == 201

        response = test_client.patch(
            f"/measurements/devices/{device_payload['tag']}",
            json=device_payload_updated,
        )
        response_json = response.json()
        assert response.status_code == 202
        assert response_json["tag"] == device_payload_updated["tag"]
        assert response_json["vendor"] == "Generic Sensing Ltd."
        assert response_json["model"] == "Fantastic Mystery Machine"

    def test_create_delete_device(self, test_client, device_payload):
        response = test_client.post("/measurements/devices",
                                    json=device_payload)
        assert response.status_code == 201

        response = test_client.delete(
            f"/measurements/devices/{device_payload['tag']}")
        assert response.status_code == 204

        response = test_client.get(
            f"/measurements/devices/{device_payload['tag']}")
        assert response.status_code == 404

    def test_get_device_not_found(self, test_client, device_tag):
        response = test_client.get(
            f"/measurements/devices/{device_tag}")
        assert response.status_code == 404

    def test_create_device_wrong_payload(self, test_client):
        response = test_client.post("/measurements/devices/", json={})
        assert response.status_code == 422

    def test_create_update_device_wrong_payload(
        self, test_client, device_tag, device_payload, device_payload_updated
    ):
        response = test_client.post("/measurements/devices/",
                                    json=device_payload)
        assert response.status_code == 201
        device_payload_updated["vendor"] = (
            True
        )
        response = test_client.patch(
            f"/measurements/devices/{device_payload['tag']}",
            json=device_payload_updated,
        )
        response = test_client.patch(
            f"/measurements/devices/{device_tag}", json=device_payload_updated
        )
        assert response.status_code == 422

    def test_update_user_doesnt_exist(
        self, test_client, device_tag, device_payload_updated
    ):
        response = test_client.patch(
            f"/measurements/devices/{device_tag}", json=device_payload_updated
        )
        assert response.status_code == 404
