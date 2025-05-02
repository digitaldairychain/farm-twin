# Duplicate key test

class TestSensors:
    def test_create_get_sensor(self, test_client, sensor_payload):
        response = test_client.post("/measurements/sensors",
                                    json=sensor_payload)
        response_json = response.json()
        assert response.status_code == 201

        print(response_json['ft'])
        response = test_client.get(
            f"/measurements/sensors/?ft={response_json['ft']}")
        assert response.status_code == 200
        assert len(response.json()["sensors"]) == 1
        response_json = response.json()["sensors"][0]
        assert response_json["measurement"] == sensor_payload["measurement"]

    def test_create_update_sensor(
        self, test_client, sensor_payload, sensor_payload_updated
    ):
        response = test_client.post("/measurements/sensors/",
                                    json=sensor_payload)
        response_json = response.json()
        assert response.status_code == 201

        sensor_id = response_json['ft']

        response = test_client.patch(
            f"/measurements/sensors/{sensor_id}",
            json=sensor_payload_updated,
        )
        response_json = response.json()
        assert response.status_code == 202
        assert response_json["serial"] == sensor_payload_updated["serial"]
        assert response_json["device"] == sensor_payload_updated["device"]
        assert response_json["measurement"] == sensor_payload_updated["measurement"]

    def test_create_delete_sensor(self, test_client, sensor_payload):
        response = test_client.post("/measurements/sensors",
                                    json=sensor_payload)
        response_json = response.json()
        assert response.status_code == 201

        sensor_id = response_json['ft']

        response = test_client.delete(
            f"/measurements/sensors/{sensor_id}")
        assert response.status_code == 204

        response = test_client.get(
            f"/measurements/sensors/?ft={sensor_id}")
        assert response.status_code == 404

    def test_get_sensor_not_found(self, test_client, object_id):
        response = test_client.get(
            f"/measurements/sensors/?ft={object_id}")
        assert response.status_code == 404

    def test_create_sensor_wrong_payload(self, test_client):
        response = test_client.post("/measurements/sensors/", json={})
        assert response.status_code == 422

    def test_create_update_sensor_wrong_payload(
        self, test_client, sensor_payload, sensor_payload_updated
    ):
        response = test_client.post("/measurements/sensors/",
                                    json=sensor_payload)
        response_json = response.json()
        assert response.status_code == 201

        sensor_id = response_json['ft']

        sensor_payload_updated["measurement"] = (
            True
        )

        response = test_client.patch(
            f"/measurements/sensors/{sensor_id}", json=sensor_payload_updated
        )
        assert response.status_code == 422

    def test_update_sensor_doesnt_exist(
        self, test_client, object_id, sensor_payload_updated
    ):
        response = test_client.patch(
            f"/measurements/sensors/{object_id}", json=sensor_payload_updated
        )
        assert response.status_code == 404
