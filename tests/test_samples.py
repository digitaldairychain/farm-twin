from . import common

ROOT = 'measurements'
KEY = 'samples'
PATH = '/' + ROOT + '/' + KEY


class TestSamples:
    def test_create_get_sample(self, test_client, sample_payload):
        common.create_get(test_client, PATH,
                          sample_payload, KEY)

    def test_create_delete_sample(self, test_client, sample_payload):
        common.create_delete(test_client, PATH,
                             sample_payload, KEY)

    def test_get_sample_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_sample_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_duplicate_sample(self, test_client, sample_payload):
        common.create_duplicate(test_client, PATH, sample_payload, KEY)
