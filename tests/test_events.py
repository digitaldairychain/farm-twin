class TestEvents:

    class TestWeight:
        def test_create_weight_event(self, test_client, weight_payload):
            response = test_client.post("/events/weight",
                                        json=weight_payload)
            response_json = response.json()
            assert response.status_code == 201
            print(response_json)
            response = test_client.get(
                f"/events/weight/?id={response_json['id']}")
            assert response.status_code == 200
            assert response_json["animal"] == weight_payload["animal"]
            assert response_json["device"] == weight_payload["device"]
            assert response_json["timeOffFeed"] == weight_payload["timeOffFeed"]

        def test_create_delete_weight_event(self, test_client, weight_payload):
            response = test_client.post("/events/weight",
                                        json=weight_payload)
            response_json = response.json()
            assert response.status_code == 201

            weight_event_id = response_json['id']

            response = test_client.delete(
                f"/events/weight/{weight_event_id}")
            assert response.status_code == 204

            response = test_client.get(
                f"/events/weight?id={weight_event_id}")
            assert response.status_code == 404

        def test_get_weight_event_not_found(self, test_client, object_id):
            response = test_client.get(
                f"/events/weight/?id={object_id}")
            assert response.status_code == 404

        def test_create_weight_event_wrong_payload(self, test_client):
            response = test_client.post("/events/weight/", json={})
            assert response.status_code == 422
