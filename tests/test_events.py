class TestEvents:

    class TestWeight:
        def test_create_weight_event(self, test_client, weight_payload, check_object_similarity):
            response = test_client.post("/events/weight",
                                        json=weight_payload)
            response_json = response.json()
            assert response.status_code == 201
            response = test_client.get(
                f"/events/weight/?ft={response_json['ft']}")
            assert response.status_code == 200
            check_object_similarity(weight_payload, response_json)

        def test_create_delete_weight_event(self, test_client, weight_payload):
            response = test_client.post("/events/weight",
                                        json=weight_payload)
            response_json = response.json()
            assert response.status_code == 201

            weight_event_id = response_json['ft']

            response = test_client.delete(
                f"/events/weight/{weight_event_id}")
            assert response.status_code == 204

            response = test_client.get(
                f"/events/weight?ft={weight_event_id}")
            assert response.status_code == 404

        def test_get_weight_event_not_found(self, test_client, object_id):
            response = test_client.get(
                f"/events/weight/?ft={object_id}")
            assert response.status_code == 404

        def test_create_weight_event_wrong_payload(self, test_client):
            response = test_client.post("/events/weight/", json={})
            assert response.status_code == 422
