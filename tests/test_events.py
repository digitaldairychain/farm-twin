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
            common.create_delete(test_client, PATH,
                                 weight_payload, KEY)

        def test_get_weight_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, PATH, object_id)

        def test_create_weight_event_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, PATH)
