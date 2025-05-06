# Duplicate key test

class TestAnimals:
    def test_create_get_animal(self, test_client, animal_payload):
        response = test_client.post("/things/animals",
                                    json=animal_payload)
        response_json = response.json()
        assert response.status_code == 201

        response = test_client.get(
            f"/things/animals/?ft={response_json['ft']}")
        assert response.status_code == 200
        assert len(response.json()["animals"]) == 1
        response_json = response.json()["animals"][0]
        assert response_json['identifier'] == animal_payload['identifier']
        assert response_json['gender'] == animal_payload['gender']
        assert response_json['specie'] == animal_payload['specie']

    def test_create_update_animal(
        self, test_client, animal_payload, animal_payload_updated
    ):
        response = test_client.post("/things/animals/",
                                    json=animal_payload)
        response_json = response.json()
        assert response.status_code == 201

        animal_id = response_json['ft']
        print(animal_id)
        response = test_client.patch(
            f"/things/animals/{animal_id}",
            json=animal_payload_updated,
        )
        response_json = response.json()
        assert response.status_code == 202
        assert response_json['identifier'] == animal_payload_updated['identifier']
        assert response_json['gender'] == animal_payload_updated['gender']
        assert response_json['specie'] == animal_payload_updated['specie']

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
