from . import common


class TestSamples:
    def test_create_get_sample(self, test_client, setup_sample):
        path, header, key, data = setup_sample
        common.create_get(test_client, path, header, data, key)

    def test_create_delete_sample(self, test_client, setup_sample):
        path, header, key, data = setup_sample
        common.create_delete(test_client, path, header, data, key)

    def test_get_sample_not_found(self, test_client, object_id, setup_sample):
        path, header, _, _ = setup_sample
        common.get_not_found(test_client, path, header, object_id)

    def test_create_sample_wrong_payload(self, test_client, setup_sample):
        path, header, _, _ = setup_sample
        common.create_wrong_payload(test_client, path, header)

    def test_create_duplicate_sample(self, test_client, setup_sample):
        path, header, key, data = setup_sample
        common.create_duplicate(test_client, path, header, data, key)
