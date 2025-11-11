from . import common


class TestAnimals:
    def test_create_get_animal(self, test_client, setup_animal):
        path, header, key, data = setup_animal
        common.create_get(test_client, path, header, data, key)

    def test_create_update_animal(
        self, test_client, setup_animal, animal_data_updated
    ):
        path, header, key, data = setup_animal
        common.create_get_update(
            test_client, path, header, data, animal_data_updated, key
        )

    def test_create_delete_animal(self, test_client, setup_animal):
        path, header, key, data = setup_animal
        common.create_delete(test_client, path, header, data, key)

    def test_get_animal_not_found(self, test_client, setup_animal, object_id):
        path, header, _, _ = setup_animal
        common.get_not_found(test_client, path, header, object_id)

    def test_create_animal_wrong_payload(self, test_client, setup_animal):
        path, header, _, _ = setup_animal
        common.create_wrong_payload(test_client, path, header)

    def test_create_update_animal_wrong_payload(
        self, test_client, setup_animal, animal_data_updated
    ):
        path, header, key, data = setup_animal
        animal_data_updated["gender"] = True
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            animal_data_updated,
            key,
            expected_code=422,
        )

    def test_create_animal_incorrect_enum(self, test_client, setup_animal):
        path, header, key, data = setup_animal
        data["productionPurpose"] = "Astronaut"
        common.create_get(
            test_client, path, header, data, key, expected_code=422
        )

    def test_update_animal_doesnt_exist(
        self, test_client, object_id, setup_animal, animal_data_updated
    ):
        path, header, _, _ = setup_animal
        common.update_doesnt_exist(
            test_client, path, header, animal_data_updated, object_id
        )
