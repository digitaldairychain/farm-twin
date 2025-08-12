from . import common

ROOT = "events"


class TestEvents:

    class TestFeeding:
        class TestFeedIntake:
            key = "feed_intake"
            path = "/" + ROOT + "/feeding/" + key

            def test_create_feed_intake_event(self, test_client, feed_intake_payload):
                common.create_get(test_client, self.path,
                                  feed_intake_payload, self.key)

            def test_create_delete_feed_intake_event(
                self, test_client, feed_intake_payload
            ):
                common.create_delete(test_client, self.path,
                                     feed_intake_payload, self.key)

            def test_get_feed_intake_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_feed_intake_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

    class TestWithdrawal:
        key = "withdrawal"
        path = "/" + ROOT + "/" + key

        def test_create_withdrawal_event(self, test_client, withdrawal_payload):
            common.create_get(test_client, self.path,
                              withdrawal_payload, self.key)

        def test_create_delete_withdrawal_event(self, test_client, withdrawal_payload):
            common.create_delete(test_client, self.path,
                                 withdrawal_payload, self.key)

        def test_get_feed_intake_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_feed_intake_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)

    class TestMovement:
        class TestArrival:
            key = "arrival"
            path = "/" + ROOT + "/movement/" + key

            def test_create_arrival_movement_event(self, test_client, arrival_payload):
                common.create_get(test_client, self.path,
                                  arrival_payload, self.key)

            def test_create_delete_arrival_movement_event(
                self, test_client, arrival_payload
            ):
                common.create_delete(test_client, self.path,
                                     arrival_payload, self.key)

            def test_get_arrival_movement_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_arrival_movement_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestBirth:
            key = "birth"
            path = "/" + ROOT + "/movement/" + key

            def test_create_birth_movement_event(self, test_client, birth_payload):
                common.create_get(test_client, self.path,
                                  birth_payload, self.key)

            def test_create_delete_birth_movement_event(
                self, test_client, birth_payload
            ):
                common.create_delete(test_client, self.path,
                                     birth_payload, self.key)

            def test_get_birth_movement_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_birth_movement_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestDeath:
            key = "death"
            path = "/" + ROOT + "/movement/" + key

            def test_create_death_movement_event(self, test_client, death_payload):
                common.create_get(test_client, self.path,
                                  death_payload, self.key)

            def test_create_delete_death_movement_event(
                self, test_client, death_payload
            ):
                common.create_delete(test_client, self.path,
                                     death_payload, self.key)

            def test_get_death_movement_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_death_movement_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestDeparture:
            key = "departure"
            path = "/" + ROOT + "/movement/" + key

            def test_create_departure_movement_event(
                self, test_client, departure_payload
            ):
                common.create_get(test_client, self.path,
                                  departure_payload, self.key)

            def test_create_delete_departure_movement_event(
                self, test_client, departure_payload
            ):
                common.create_delete(
                    test_client, self.path, departure_payload, self.key
                )

            def test_get_departure_movement_event_not_found(
                self, test_client, object_id
            ):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_departure_movement_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

    class TestMilking:
        class TestLactationStatus:
            key = "lactation_status"
            path = "/" + ROOT + "/milking/" + key

            def test_create_lactation_status_event(
                self, test_client, lactation_status_payload
            ):
                common.create_get(
                    test_client, self.path, lactation_status_payload, self.key
                )

            def test_create_delete_lactation_status_event(
                self, test_client, lactation_status_payload
            ):
                common.create_delete(
                    test_client, self.path, lactation_status_payload, self.key
                )

            def test_get_lactation_status_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_lactation_status_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestTestDayResult:
            key = "test_day_result"
            path = "/" + ROOT + "/milking/" + key

            def test_create_test_day_result_event(
                self, test_client, test_day_result_payload
            ):
                common.create_get(
                    test_client, self.path, test_day_result_payload, self.key
                )

            def test_create_delete_test_day_result_event(
                self, test_client, test_day_result_payload
            ):
                common.create_delete(
                    test_client, self.path, test_day_result_payload, self.key
                )

            def test_get_test_day_result_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_test_day_result_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestDryingOff:
            key = "drying_off"
            path = "/" + ROOT + "/milking/" + key

            def test_create_drying_off_event(self, test_client, drying_off_payload):
                common.create_get(test_client, self.path,
                                  drying_off_payload, self.key)

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

        class TestMilkingVisit:
            key = "visit"
            path = "/" + ROOT + "/milking/" + key

            def test_create_milking_visit_event(
                self, test_client, milking_visit_payload
            ):
                common.create_get(
                    test_client, self.path, milking_visit_payload, self.key
                )

            def test_create_delete_milking_visit_event(
                self, test_client, milking_visit_payload
            ):
                common.create_delete(
                    test_client, self.path, milking_visit_payload, self.key
                )

            def test_get_milking_visit_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_milking_visit_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

    class TestObservations:
        class TestCarcass:
            key = "carcass"
            path = "/" + ROOT + "/observations/" + key

            def test_create_carcass_event(self, test_client, carcass_payload):
                common.create_get(test_client, self.path,
                                  carcass_payload, self.key)

            def test_create_delete_carcass_event(self, test_client, carcass_payload):
                common.create_delete(test_client, self.path,
                                     carcass_payload, self.key)

            def test_get_carcass_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_carcass_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestHealthStatus:
            key = "health_status"
            path = "/" + ROOT + "/observations/" + key

            def test_create_health_status_event(
                self, test_client, health_status_payload
            ):
                common.create_get(
                    test_client, self.path, health_status_payload, self.key
                )

            def test_create_delete_health_status_event(
                self, test_client, health_status_payload
            ):
                common.create_delete(
                    test_client, self.path, health_status_payload, self.key
                )

            def test_get_health_status_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_health_status_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestPositionStatus:
            key = "position"
            path = "/" + ROOT + "/observations/" + key

            def test_create_position_event(self, test_client, position_payload):
                common.create_get(test_client, self.path,
                                  position_payload, self.key)

            def test_create_delete_position_event(self, test_client, position_payload):
                common.create_delete(test_client, self.path,
                                     position_payload, self.key)

            def test_get_position_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_position_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

        class TestReproStatus:
            key = "repro_status"
            path = "/" + ROOT + "/observations/" + key

            def test_create_repro_status_event(self, test_client, repro_status_payload):
                common.create_get(
                    test_client, self.path, repro_status_payload, self.key
                )

            def test_create_delete_repro_status_event(
                self, test_client, repro_status_payload
            ):
                common.create_delete(
                    test_client, self.path, repro_status_payload, self.key
                )

            def test_get_repro_status_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_repro_status_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

    class TestAttention:
        key = "attention"
        path = "/" + ROOT + "/" + key

        def test_create_attention_event(self, test_client, attention_payload):
            common.create_get(test_client, self.path,
                              attention_payload, self.key)

        def test_create_delete_attention_event(self, test_client, attention_payload):
            common.create_delete(test_client, self.path,
                                 attention_payload, self.key)

        def test_get_attention_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_attention_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)

    class TestPerformance:
        class TestConformation:
            key = "conformation"
            path = "/" + ROOT + "/performance/" + key

            def test_create_conformation_event(self, test_client, conformation_payload):
                common.create_get(test_client, self.path,
                                  conformation_payload, self.key)

            def test_create_delete_conformation_event(
                self, test_client, conformation_payload
            ):
                common.create_delete(test_client, self.path,
                                     conformation_payload, self.key)

            def test_get_conformation_event_event_not_found(self, test_client, object_id):
                common.get_not_found(test_client, self.path, object_id)

            def test_create_conformation_event_wrong_payload(self, test_client):
                common.create_wrong_payload(test_client, self.path)

    class TestWeight:
        key = "weight"
        path = "/" + ROOT + "/performance/" + key

        def test_create_weight_event(self, test_client, weight_payload):
            common.create_get(test_client, self.path, weight_payload, self.key)

        def test_create_delete_weight_event(self, test_client, weight_payload):
            common.create_delete(test_client, self.path,
                                 weight_payload, self.key)

        def test_get_weight_event_not_found(self, test_client, object_id):
            common.get_not_found(test_client, self.path, object_id)

        def test_create_weight_event_wrong_payload(self, test_client):
            common.create_wrong_payload(test_client, self.path)
