from . import common

ROOT = 'measurements'
KEY = 'samples'
PATH = '/' + ROOT + '/' + KEY


class TestSamples:
    def test_create_get_sample(self, test_client, sample_payload):
        common.create_get(test_client, PATH,
                          sample_payload, KEY)

    def test_create_delete_sample(self, test_client, sample_payload):
        response = test_client.post("/measurements/samples",
                                    json=sample_payload)
        response_json = response.json()
        assert response.status_code == 201
        sample_id = response_json['ft']
        response = test_client.delete(
            f"/measurements/samples/{sample_id}")
        assert response.status_code == 204
        response = test_client.get(
            f"/measurements/samples/?ft={sample_id}")
        assert response.status_code == 404

    def test_get_sample_not_found(self, test_client, object_id):
        response = test_client.get(
            f"/measurements/samples/?ft={object_id}")
        assert response.status_code == 404

    def test_create_sample_wrong_payload(self, test_client):
        response = test_client.post("/measurements/samples/", json={})
        assert response.status_code == 422
