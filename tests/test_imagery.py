from bson.objectid import ObjectId

from . import common


class TestImagery:
    def test_create_get_image(self, test_client, setup_image):
        path, header, data, filename = setup_image
        response = test_client.post(
            path, headers=header, files={"file": (filename, data)}
        )
        assert response.status_code == 201
        ft = response.json()["ft"]
        response = test_client.get(path + f"/?ft={ft}", headers=header)
        assert response.status_code == 200

    def test_create_delete_image(self, test_client, setup_image):
        path, header, data, filename = setup_image
        response = test_client.post(
            path, headers=header, files={"file": (filename, data)}
        )
        assert response.status_code == 201
        ft = response.json()["ft"]
        response = test_client.delete(path + f"/{ft}", headers=header)
        assert response.status_code == 200

    def test_create_get_image_alternative(
        self, test_client, setup_image, setup_image_alternative
    ):
        path, header, _, _ = setup_image
        data, filename = setup_image_alternative
        response = test_client.post(
            path, headers=header, files={"file": (filename, data)}
        )
        assert response.status_code == 201
        ft = response.json()["ft"]
        response = test_client.get(path + f"/?ft={ft}", headers=header)
        assert response.status_code == 200

    def test_get_image_doesnt_exist(self, test_client, setup_image):
        path, header, _, _ = setup_image
        response = test_client.get(
            path + f"/?ft={str(ObjectId())}", headers=header
        )
        assert response.status_code == 404

    def test_delete_image_doesnt_exist(self, test_client, setup_image):
        path, header, _, _ = setup_image
        response = test_client.delete(
            path + f"/{str(ObjectId())}", headers=header
        )
        assert response.status_code == 404


class TestMetadata:
    def test_create_get_metadata(self, test_client, setup_metadata):
        path, header, key, data = setup_metadata
        common.create_get(test_client, path, header, data, key)

    def test_create_delete_metadata(self, test_client, setup_metadata):
        path, header, key, data = setup_metadata
        common.create_delete(test_client, path, header, data, key)

    def test_get_metadata_not_found(
        self, test_client, setup_metadata, object_id
    ):
        path, header, _, _ = setup_metadata
        common.get_not_found(test_client, path, header, object_id)

    def test_create_metadata_wrong_payload(self, test_client, setup_metadata):
        path, header, _, _ = setup_metadata
        common.create_wrong_payload(test_client, path, header)
