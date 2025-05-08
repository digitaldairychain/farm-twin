from . import common

ROOT = 'events'
KEY = 'weights'
PATH = '/' + ROOT + '/' + KEY


class TestEvents:

    class TestWeight:
        def test_create_weight_event(self, test_client, weight_payload):
            common.create_get(test_client, PATH,
                              weight_payload, KEY)

        def test_create_delete_weight_event(self, test_client, weight_payload):
            response = test_client.post("/events/weights",
                                        json=weight_payload)
            response_json = response.json()
            assert response.status_code == 201

            weight_event_id = response_json['ft']

            response = test_client.delete(
                f"/events/weights/{weight_event_id}")
            assert response.status_code == 204

            response = test_client.get(
                f"/events/weights?ft={weight_event_id}")
            assert response.status_code == 404

        def test_get_weight_event_not_found(self, test_client, object_id):
            response = test_client.get(
                f"/events/weights/?ft={object_id}")
            assert response.status_code == 404

        def test_create_weight_event_wrong_payload(self, test_client):
            response = test_client.post("/events/weights/", json={})
            assert response.status_code == 422
