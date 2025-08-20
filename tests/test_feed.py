from . import common

ROOT = "things"
KEY = "feed"
PATH = "/" + ROOT + "/" + KEY


class TestAnimals:
    def test_create_get_feed(self, test_client, feed_payload):
        common.create_get(test_client, PATH, feed_payload, KEY)

    def test_create_update_feed(self, test_client, feed_payload, feed_payload_updated):
        common.create_get_update(
            test_client, PATH, feed_payload, feed_payload_updated, KEY
        )

    def test_create_delete_feed(self, test_client, feed_payload):
        common.create_delete(test_client, PATH, feed_payload, KEY)

    def test_get_feed_not_found(self, test_client, object_id):
        common.get_not_found(test_client, PATH, object_id)

    def test_create_feed_wrong_payload(self, test_client):
        common.create_wrong_payload(test_client, PATH)

    def test_create_update_feed_wrong_payload(
        self, test_client, feed_payload, feed_payload_updated
    ):
        feed_payload_updated["name"] = True
        common.create_get_update(
            test_client,
            PATH,
            feed_payload,
            feed_payload_updated,
            KEY,
            expected_code=422,
        )

    def test_create_feed_incorrect_enum(self, test_client, feed_payload):
        feed_payload["category"] = "BreakfastCereal"
        common.create_get(test_client, PATH, feed_payload, KEY, expected_code=422)

    def test_update_feed_doesnt_exist(
        self, test_client, object_id, feed_payload_updated
    ):
        common.update_doesnt_exist(test_client, PATH, feed_payload_updated, object_id)
