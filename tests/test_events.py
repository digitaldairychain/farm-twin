from . import common

ROOT = "events"


class TestEvents:
    class TestWeight:
        key = "weight"
        path = "/" + ROOT + "/" + key

        def test_create_weight_event(self, test_client, weight_payload):
            common.create_get(test_client, self.path, weight_payload, self.key)

        def test_create_delete_weight_event(self, test_client, weight_payload):
            common.create_delete(test_client, self.path, weight_payload, self.key)

        def test_get_weight_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_weight_event_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)

    class TestFeedIntake:
        key = "feed_intake"
        path = "/" + ROOT + "/" + key

        def test_create_feed_intake_event(self, test_client, feed_intake_payload):
            common.create_get(test_client, self.path, feed_intake_payload, self.key)

        def test_create_delete_feed_intake_event(
            self, test_client, feed_intake_payload
        ):
            common.create_delete(test_client, self.path, feed_intake_payload, self.key)

        def test_get_feed_intake_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_feed_intake_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)

    class TestWithdrawal:
        key = "withdrawal"
        path = "/" + ROOT + "/" + key

        def test_create_withdrawal_event(self, test_client, withdrawal_payload):
            common.create_get(test_client, self.path, withdrawal_payload, self.key)

        def test_create_delete_withdrawal_event(self, test_client, withdrawal_payload):
            common.create_delete(test_client, self.path, withdrawal_payload, self.key)

        def test_get_feed_intake_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_feed_intake_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)

    class TestConformation:
        key = "conformation"
        path = "/" + ROOT + "/" + key

        def test_create_conformation_event(self, test_client, conformation_payload):
            common.create_get(test_client, self.path, conformation_payload, self.key)

        def test_create_delete_conformation_event(
            self, test_client, conformation_payload
        ):
            common.create_delete(test_client, self.path, conformation_payload, self.key)

        def test_get_feed_intake_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_feed_intake_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)

    class TestMovement:
        class TestArrival:
            key = "arrival"
            path = "/" + ROOT + "/movement/" + key

            def test_create_movement_event(self, test_client, arrival_payload):
                common.create_get(test_client, self.path, arrival_payload, self.key)

            def test_create_delete_drying_off_event(self, test_client, arrival_payload):
                common.create_delete(test_client, self.path, arrival_payload, self.key)

            def test_get_drying_off_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_drying_off_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

    class TestMilking:
        class TestDryingOff:
            key = "drying_off"
            path = "/" + ROOT + "/milking/" + key

            def test_create_drying_off_event(self, test_client, drying_off_payload):
                common.create_get(test_client, self.path, drying_off_payload, self.key)

            def test_create_delete_drying_off_event(
                self, test_client, drying_off_payload
            ):
                common.create_delete(
                    test_client, self.path, drying_off_payload, self.key
                )

            def test_get_drying_off_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_drying_off_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)
