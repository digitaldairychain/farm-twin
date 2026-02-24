from . import common


class TestImages:
    def test_create_get_image(self, test_client, setup_image):
        path, header, key, data = setup_image
        common.create_get(test_client, path, header, data, key)

    def test_create_delete_image(self, test_client, setup_image):
        path, header, key, data = setup_image
        common.create_delete(test_client, path, header, data, key)

    def test_get_image_not_found(self, test_client, setup_image, object_id):
        path, header, _, _ = setup_image
        common.get_not_found(test_client, path, header, object_id)

    def test_create_image_wrong_payload(self, test_client, setup_image):
        path, header, _, _ = setup_image
        common.create_wrong_payload(test_client, path, header)
