import pytest
from . import common


class TestImagery:
    def test_create_get_image(self, test_client, setup_image):
        path, header, data, filename = setup_image
        response = test_client.post(path, headers=header, files={'file': (filename, data)})
        assert response.status_code == 201
        ft = response.json()["ft"]
        response = test_client.get(path + f"/?ft={ft}", headers=header)
        assert response.status_code == 200
        #compare file to check the same


    def test_create_delete_image(self, test_client, setup_image):
        path, header, data, filename = setup_image
        response = test_client.post(path, headers=header, files={'file': (filename, data)})
        assert response.status_code == 201
        ft = response.json()["ft"]
        response = test_client.delete(path + f"/{ft}", headers=header)
        assert response.status_code == 200

    def test_create_get_image_alternative(self, test_client, setup_image, setup_image_alternative):
        path, header, _, _ = setup_image
        data, filename = setup_image_alternative
        response = test_client.post(path, headers=header, files={'file': (filename, data)})
        assert response.status_code == 201
        ft = response.json()["ft"]
        response = test_client.get(path + f"/?ft={ft}", headers=header)
        assert response.status_code == 200

#TODO: delete a file that doesn't exist
#TODO: find a file that doesn't exist
#TODO: documentation