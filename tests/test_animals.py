# TODO: Duplicate key test
from . import common

ROOT = 'things'
KEY = 'animals'
PATH = '/' + ROOT + '/' + KEY


class TestAnimals:
    def test_create_get_animal(self, test_client, animal_payload):
        common.create_get(test_client, PATH,
                          animal_payload, KEY)

    def test_create_update_animal(
        self, test_client, animal_payload, animal_payload_updated,
        check_object_similarity
    ):
        response = test_client.post("/things/animals/",
                                    json=animal_payload)
        response_json = response.json()
        assert response.status_code == 201
        check_object_similarity(animal_payload, response_json)
        animal_id = response_json['ft']
        response = test_client.patch(
            f"/things/animals/{animal_id}",
            json=animal_payload_updated,
        )
        response_json = response.json()
        assert response.status_code == 202
        check_object_similarity(animal_payload_updated, response_json)

    def test_create_delete_animal(self, test_client, animal_payload):
        response = test_client.post("/things/animals",
                                    json=animal_payload)
        response_json = response.json()
        assert response.status_code == 201
        animal_id = response_json['ft']
        response = test_client.delete(
            f"/things/animals/{animal_id}")
        assert response.status_code == 204
        response = test_client.get(
            f"/things/animals/?ft={animal_id}")
        assert response.status_code == 404

    def test_get_animal_not_found(self, test_client, object_id):
        response = test_client.get(
            f"/things/animals/?ft={object_id}")
        assert response.status_code == 404

    def test_create_animal_wrong_payload(self, test_client):
        response = test_client.post("/things/animals/", json={})
        assert response.status_code == 422

    def test_create_update_animal_wrong_payload(
        self, test_client, animal_payload, animal_payload_updated
    ):
        response = test_client.post("/things/animals/",
                                    json=animal_payload)
        response_json = response.json()
        assert response.status_code == 201
        animal_id = response_json['ft']
        animal_payload_updated["gender"] = (
            True
        )
        response = test_client.patch(
            f"/things/animals/{animal_id}", json=animal_payload_updated
        )
        assert response.status_code == 422

    def test_update_animal_doesnt_exist(
        self, test_client, object_id, animal_payload_updated
    ):
        response = test_client.patch(
            f"/things/animals/{object_id}", json=animal_payload_updated
        )
        assert response.status_code == 404
