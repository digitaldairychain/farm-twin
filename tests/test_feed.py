from . import common


class TestFeed:
    def test_create_get_feed(self, test_client, setup_feed):
        path, key, data = setup_feed
        common.create_get(test_client, path, data, key)

    def test_create_update_feed(self, test_client, setup_feed, feed_payload_updated):
        path, key, data = setup_feed
        common.create_get_update(
            test_client, path, data, feed_payload_updated, key
        )

    def test_create_delete_feed(self, test_client, setup_feed):
        path, key, data = setup_feed
        common.create_delete(test_client, path, data, key)

    def test_get_feed_not_found(self, test_client, object_id, setup_feed):
        path, _, _ = setup_feed
        common.get_not_found(test_client, path, object_id)

    def test_create_feed_wrong_payload(self, test_client, setup_feed):
        path, _, _ = setup_feed
        common.create_wrong_payload(test_client, path)

    def test_create_update_feed_wrong_payload(
        self, test_client, setup_feed, feed_payload_updated
    ):
        path, key, data = setup_feed
        feed_payload_updated["name"] = True
        common.create_get_update(
            test_client,
            path,
            data,
            feed_payload_updated,
            key,
            expected_code=422,
        )

    def test_create_feed_incorrect_enum(self, test_client, setup_feed):
        path, key, data = setup_feed
        data["category"] = "BreakfastCereal"
        common.create_get(test_client, path, data,
                          key, expected_code=422)

    def test_update_feed_doesnt_exist(
        self, test_client, object_id, feed_payload_updated, setup_feed
    ):
        path, _, _ = setup_feed
        common.update_doesnt_exist(
            test_client, path, feed_payload_updated, object_id)
