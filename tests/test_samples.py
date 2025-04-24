class TestSamples:
    def test_create_get_sample(self, test_client, sample_payload, convert_timestamp):
        response = test_client.post("/measurements/samples",
                                    json=sample_payload)
        response_json = response.json()
        assert response.status_code == 201

        sample_id = response_json['id']

        response = test_client.get(
            f"/measurements/samples/?id={sample_id}")
        assert response.status_code == 200
        assert len(response.json()["samples"]) == 1
        response_json = response.json()["samples"][0]
        assert response_json["sensor"] == sample_payload["sensor"]
        server_ts, local_ts = convert_timestamp(
            response_json["timestamp"],
            sample_payload["timestamp"]
        )
        assert server_ts == local_ts
        assert response_json["value"] == sample_payload["value"]
        assert response_json["predicted"] == sample_payload["predicted"]

    def test_create_delete_sample(self, test_client, sample_payload):
        response = test_client.post("/measurements/samples",
                                    json=sample_payload)
        response_json = response.json()
        assert response.status_code == 201

        sample_id = response_json['id']

        response = test_client.delete(
            f"/measurements/samples/{sample_id}")
        assert response.status_code == 204

        response = test_client.get(
            f"/measurements/samples/?id={sample_id}")
        assert response.status_code == 404

    def test_get_sample_not_found(self, test_client, object_id):
        response = test_client.get(
            f"/measurements/samples/?id={object_id}")
        assert response.status_code == 404

    def test_create_sample_wrong_payload(self, test_client):
        response = test_client.post("/measurements/samples/", json={})
        assert response.status_code == 422
