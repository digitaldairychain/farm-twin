from . import common


class TestFeedStorage:
    def test_create_get_feed_storage(self, test_client, setup_feed_storage):
        path, header, key, data = setup_feed_storage
        common.create_get(test_client, path, header, data, key)

    def test_create_update_feed_storage(
        self, test_client, setup_feed_storage, feed_storage_payload_updated
    ):
        path, header, key, data = setup_feed_storage
        common.create_get_update(
            test_client, path, header, data, feed_storage_payload_updated, key
        )

    def test_create_delete_feed_storage(self, test_client, setup_feed_storage):
        path, header, key, data = setup_feed_storage
        common.create_delete(test_client, path, header, data, key)

    def test_get_feed_storage_not_found(
        self, test_client, object_id, setup_feed_storage
    ):
        path, header, _, _ = setup_feed_storage
        common.get_not_found(test_client, path, header, object_id)

    def test_create_feed_storage_wrong_payload(
        self, test_client, setup_feed_storage
    ):
        path, header, _, _ = setup_feed_storage
        common.create_wrong_payload(test_client, path, header)

    def test_create_update_feed_storage_wrong_payload(
        self, test_client, setup_feed_storage, feed_storage_payload_updated
    ):
        path, header, key, data = setup_feed_storage
        feed_storage_payload_updated["feedId"] = True
        common.create_get_update(
            test_client,
            path,
            header,
            data,
            feed_storage_payload_updated,
            key,
            expected_code=422,
        )

    def test_update_feed_storage_doesnt_exist(
        self,
        test_client,
        object_id,
        feed_storage_payload_updated,
        setup_feed_storage,
    ):
        path, header, _, _ = setup_feed_storage
        common.update_doesnt_exist(
            test_client, path, header, feed_storage_payload_updated, object_id
        )
