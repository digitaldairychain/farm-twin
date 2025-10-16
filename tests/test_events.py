from . import common

ROOT = "events"


class TestEvents:
    class TestFeeding:
        class TestFeedIntake:
            def test_create_feed_intake_event(self, test_client, setup_feed_intake):
                path, key, data = setup_feed_intake
                common.create_get(test_client, path, data, key)

            def test_create_delete_feed_intake_event(
                self, test_client, setup_feed_intake
            ):
                path, key, data = setup_feed_intake
                common.create_delete(test_client, path, data, key)

            def test_get_feed_intake_event_not_found(
                self, test_client, object_id, setup_feed_intake
            ):
                path, _, _ = setup_feed_intake
                common.get_not_found(test_client, path, object_id)

            def test_create_feed_intake_wrong_payload(
                self, test_client, setup_feed_intake
            ):
                path, _, _ = setup_feed_intake
                common.create_wrong_payload(test_client, path)

    class TestWithdrawal:
        def test_create_withdrawal_event(self, test_client, setup_withdrawal):
            path, key, data = setup_withdrawal
            common.create_get(test_client, path, data, key)

        def test_create_delete_withdrawal_event(self, test_client, setup_withdrawal):
            path, key, data = setup_withdrawal
            common.create_delete(test_client, path, data, key)

        def test_get_withdrawal_event_not_found(
            self, test_client, object_id, setup_withdrawal
        ):
            path, _, _ = setup_withdrawal
            common.get_not_found(test_client, path, object_id)

        def test_create_withdrawal_wrong_payload(self, test_client, setup_withdrawal):
            path, _, _ = setup_withdrawal
            common.create_wrong_payload(test_client, path)

    class TestMovement:
        class TestArrival:
            def test_create_arrival_event(self, test_client, setup_arrival):
                path, key, data = setup_arrival
                common.create_get(test_client, path, data, key)

            def test_create_delete_arrival_event(self, test_client, setup_arrival):
                path, key, data = setup_arrival
                common.create_delete(test_client, path, data, key)

            def test_get_arrival_event_not_found(
                self, test_client, object_id, setup_arrival
            ):
                path, _, _ = setup_arrival
                common.get_not_found(test_client, path, object_id)

            def test_create_arrival_wrong_payload(self, test_client, setup_arrival):
                path, _, _ = setup_arrival
                common.create_wrong_payload(test_client, path)

        class TestBirth:
            def test_create_birth_event(self, test_client, setup_birth):
                path, key, data = setup_birth
                common.create_get(test_client, path, data, key)

            def test_create_delete_birth_event(self, test_client, setup_birth):
                path, key, data = setup_birth
                common.create_delete(test_client, path, data, key)

            def test_get_birth_event_not_found(
                self, test_client, object_id, setup_birth
            ):
                path, _, _ = setup_birth
                common.get_not_found(test_client, path, object_id)

            def test_create_birth_wrong_payload(self, test_client, setup_birth):
                path, _, _ = setup_birth
                common.create_wrong_payload(test_client, path)

        class TestDeath:
            def test_create_death_event(self, test_client, setup_death):
                path, key, data = setup_death
                common.create_get(test_client, path, data, key)

            def test_create_delete_death_event(self, test_client, setup_death):
                path, key, data = setup_death
                common.create_delete(test_client, path, data, key)

            def test_get_death_event_not_found(
                self, test_client, object_id, setup_death
            ):
                path, _, _ = setup_death
                common.get_not_found(test_client, path, object_id)

            def test_create_death_wrong_payload(self, test_client, setup_death):
                path, _, _ = setup_death
                common.create_wrong_payload(test_client, path)

        class TestDeparture:
            def test_create_departure_event(self, test_client, setup_departure):
                path, key, data = setup_departure
                common.create_get(test_client, path, data, key)

            def test_create_delete_departure_event(self, test_client, setup_departure):
                path, key, data = setup_departure
                common.create_delete(test_client, path, data, key)

            def test_get_departure_event_not_found(
                self, test_client, object_id, setup_departure
            ):
                path, _, _ = setup_departure
                common.get_not_found(test_client, path, object_id)

            def test_create_departure_wrong_payload(self, test_client, setup_departure):
                path, _, _ = setup_departure
                common.create_wrong_payload(test_client, path)

    class TestMilking:
        class TestLactationStatus:
            def test_create_lactation_status_event(
                self, test_client, setup_lactation_status
            ):
                path, key, data = setup_lactation_status
                common.create_get(test_client, path, data, key)

            def test_create_delete_lactation_status_event(
                self, test_client, setup_lactation_status
            ):
                path, key, data = setup_lactation_status
                common.create_delete(test_client, path, data, key)

            def test_get_lactation_status_event_not_found(
                self, test_client, object_id, setup_lactation_status
            ):
                path, _, _ = setup_lactation_status
                common.get_not_found(test_client, path, object_id)

            def test_create_lactation_status_wrong_payload(
                self, test_client, setup_lactation_status
            ):
                path, _, _ = setup_lactation_status
                common.create_wrong_payload(test_client, path)

        class TestTestDayResult:
            def test_create_test_day_result_event(
                self, test_client, setup_test_day_result
            ):
                path, key, data = setup_test_day_result
                common.create_get(test_client, path, data, key)

            def test_create_delete_test_day_result_event(
                self, test_client, setup_test_day_result
            ):
                path, key, data = setup_test_day_result
                common.create_delete(test_client, path, data, key)

            def test_get_test_day_result_event_not_found(
                self, test_client, object_id, setup_test_day_result
            ):
                path, _, _ = setup_test_day_result
                common.get_not_found(test_client, path, object_id)

            def test_create_test_day_result_wrong_payload(
                self, test_client, setup_test_day_result
            ):
                path, _, _ = setup_test_day_result
                common.create_wrong_payload(test_client, path)

        class TestDryingOff:
            def test_create_drying_off_event(self, test_client, setup_drying_off):
                path, key, data = setup_drying_off
                common.create_get(test_client, path, data, key)

            def test_create_delete_drying_off_event(
                self, test_client, setup_drying_off
            ):
                path, key, data = setup_drying_off
                common.create_delete(test_client, path, data, key)

            def test_get_drying_off_event_not_found(
                self, test_client, object_id, setup_drying_off
            ):
                path, _, _ = setup_drying_off
                common.get_not_found(test_client, path, object_id)

            def test_create_drying_off_wrong_payload(
                self, test_client, setup_drying_off
            ):
                path, _, _ = setup_drying_off
                common.create_wrong_payload(test_client, path)

        class TestMilkingVisit:
            def test_create_milking_visit_event(self, test_client, setup_milking_visit):
                path, key, data = setup_milking_visit
                common.create_get(test_client, path, data, key)

            def test_create_delete_milking_visit_event(
                self, test_client, setup_milking_visit
            ):
                path, key, data = setup_milking_visit
                common.create_delete(test_client, path, data, key)

            def test_get_milking_visit_event_not_found(
                self, test_client, object_id, setup_milking_visit
            ):
                path, _, _ = setup_milking_visit
                common.get_not_found(test_client, path, object_id)

            def test_create_milking_visit_wrong_payload(
                self, test_client, setup_milking_visit
            ):
                path, _, _ = setup_milking_visit
                common.create_wrong_payload(test_client, path)

    class TestObservations:
        class TestCarcass:
            def test_create_carcass_event(self, test_client, setup_carcass):
                path, key, data = setup_carcass
                common.create_get(test_client, path, data, key)

            def test_create_delete_carcass_event(self, test_client, setup_carcass):
                path, key, data = setup_carcass
                common.create_delete(test_client, path, data, key)

            def test_get_carcass_event_not_found(
                self, test_client, object_id, setup_carcass
            ):
                path, _, _ = setup_carcass
                common.get_not_found(test_client, path, object_id)

            def test_create_carcass_wrong_payload(self, test_client, setup_carcass):
                path, _, _ = setup_carcass
                common.create_wrong_payload(test_client, path)

        class TestHealthStatus:
            def test_create_health_status_event(self, test_client, setup_health_status):
                path, key, data = setup_health_status
                common.create_get(test_client, path, data, key)

            def test_create_delete_health_status_event(
                self, test_client, setup_health_status
            ):
                path, key, data = setup_health_status
                common.create_delete(test_client, path, data, key)

            def test_get_health_status_event_not_found(
                self, test_client, object_id, setup_health_status
            ):
                path, _, _ = setup_health_status
                common.get_not_found(test_client, path, object_id)

            def test_create_health_status_wrong_payload(
                self, test_client, setup_health_status
            ):
                path, _, _ = setup_health_status
                common.create_wrong_payload(test_client, path)

        class TestPositionStatus:
            def test_create_position_event(self, test_client, setup_position):
                path, key, data = setup_position
                common.create_get(test_client, path, data, key)

            def test_create_delete_position_event(self, test_client, setup_position):
                path, key, data = setup_position
                common.create_delete(test_client, path, data, key)

            def test_get_position_event_not_found(
                self, test_client, object_id, setup_position
            ):
                path, _, _ = setup_position
                common.get_not_found(test_client, path, object_id)

            def test_create_position_wrong_payload(self, test_client, setup_position):
                path, _, _ = setup_position
                common.create_wrong_payload(test_client, path)

    class TestReproduction:
        class TestReproStatus:
            def test_create_repro_status_event(self, test_client, setup_repro_status):
                path, key, data = setup_repro_status
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_status_event(
                self, test_client, setup_repro_status
            ):
                path, key, data = setup_repro_status
                common.create_delete(test_client, path, data, key)

            def test_get_repro_status_event_not_found(
                self, test_client, object_id, setup_repro_status
            ):
                path, _, _ = setup_repro_status
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_status_wrong_payload(
                self, test_client, setup_repro_status
            ):
                path, _, _ = setup_repro_status
                common.create_wrong_payload(test_client, path)

        class TestReproDNB:
            def test_create_repro_do_not_breed_event(
                self, test_client, setup_repro_do_not_breed
            ):
                path, key, data = setup_repro_do_not_breed
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_do_not_breed_event(
                self, test_client, setup_repro_do_not_breed
            ):
                path, key, data = setup_repro_do_not_breed
                common.create_delete(test_client, path, data, key)

            def test_get_repro_do_not_breed_event_not_found(
                self, test_client, object_id, setup_repro_do_not_breed
            ):
                path, _, _ = setup_repro_do_not_breed
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_do_not_breed_wrong_payload(
                self, test_client, setup_repro_do_not_breed
            ):
                path, _, _ = setup_repro_do_not_breed
                common.create_wrong_payload(test_client, path)

        class TestReproAbortion:
            def test_create_repro_abortion_event(
                self, test_client, setup_repro_abortion
            ):
                path, key, data = setup_repro_abortion
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_abortion_event(
                self, test_client, setup_repro_abortion
            ):
                path, key, data = setup_repro_abortion
                common.create_delete(test_client, path, data, key)

            def test_get_repro_abortion_event_not_found(
                self, test_client, object_id, setup_repro_abortion
            ):
                path, _, _ = setup_repro_abortion
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_abortion_wrong_payload(
                self, test_client, setup_repro_abortion
            ):
                path, _, _ = setup_repro_abortion
                common.create_wrong_payload(test_client, path)

        class TestReproHeat:
            def test_create_repro_heat_event(self, test_client, setup_repro_heat):
                path, key, data = setup_repro_heat
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_heat_event(
                self, test_client, setup_repro_heat
            ):
                path, key, data = setup_repro_heat
                common.create_delete(test_client, path, data, key)

            def test_get_repro_heat_event_not_found(
                self, test_client, object_id, setup_repro_heat
            ):
                path, _, _ = setup_repro_heat
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_heat_wrong_payload(
                self, test_client, setup_repro_heat
            ):
                path, _, _ = setup_repro_heat
                common.create_wrong_payload(test_client, path)

        class TestReproInsemination:
            def test_create_repro_insemination_event(
                self, test_client, setup_repro_insemination
            ):
                path, key, data = setup_repro_insemination
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_insemination_event(
                self, test_client, setup_repro_insemination
            ):
                path, key, data = setup_repro_insemination
                common.create_delete(test_client, path, data, key)

            def test_get_repro_insemination_event_not_found(
                self, test_client, object_id, setup_repro_insemination
            ):
                path, _, _ = setup_repro_insemination
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_insemination_wrong_payload(
                self, test_client, setup_repro_insemination
            ):
                path, _, _ = setup_repro_insemination
                common.create_wrong_payload(test_client, path)

        class TestReproMatingRecommendation:
            def test_create_repro_mating_recommendation_event(
                self, test_client, setup_repro_mating_recommendation
            ):
                path, key, data = setup_repro_mating_recommendation
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_mating_recommendation_event(
                self, test_client, setup_repro_mating_recommendation
            ):
                path, key, data = setup_repro_mating_recommendation
                common.create_delete(test_client, path, data, key)

            def test_get_repro_mating_recommendation_event_not_found(
                self, test_client, object_id, setup_repro_mating_recommendation
            ):
                path, _, _ = setup_repro_mating_recommendation
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_mating_recommendation_wrong_payload(
                self, test_client, setup_repro_mating_recommendation
            ):
                path, _, _ = setup_repro_mating_recommendation
                common.create_wrong_payload(test_client, path)

        class TestReproParturition:
            def test_create_repro_parturition_event(
                self, test_client, setup_repro_parturition
            ):
                path, key, data = setup_repro_parturition
                common.create_get(test_client, path, data, key)

            def test_create_delete_repro_parturition_event(
                self, test_client, setup_repro_parturition
            ):
                path, key, data = setup_repro_parturition
                common.create_delete(test_client, path, data, key)

            def test_get_repro_parturition_event_not_found(
                self, test_client, object_id, setup_repro_parturition
            ):
                path, _, _ = setup_repro_parturition
                common.get_not_found(test_client, path, object_id)

            def test_create_repro_parturition_wrong_payload(
                self, test_client, setup_repro_parturition
            ):
                path, _, _ = setup_repro_parturition
                common.create_wrong_payload(test_client, path)

    class TestAttention:
        def test_create_attention_event(self, test_client, setup_attention):
            path, key, data = setup_attention
            common.create_get(test_client, path, data, key)

        def test_create_delete_attention_event(self, test_client, setup_attention):
            path, key, data = setup_attention
            common.create_delete(test_client, path, data, key)

        def test_get_attention_event_not_found(
            self, test_client, object_id, setup_attention
        ):
            path, _, _ = setup_attention
            common.get_not_found(test_client, path, object_id)

        def test_create_attention_wrong_payload(self, test_client, setup_attention):
            path, _, _ = setup_attention
            common.create_wrong_payload(test_client, path)

    class TestPerformance:
        class TestConformation:
            def test_create_conformation_event(self, test_client, setup_conformation):
                path, key, data = setup_conformation
                common.create_get(test_client, path, data, key)

            def test_create_delete_conformation_event(
                self, test_client, setup_conformation
            ):
                path, key, data = setup_conformation
                common.create_delete(test_client, path, data, key)

            def test_get_conformation_event_not_found(
                self, test_client, object_id, setup_conformation
            ):
                path, _, _ = setup_conformation
                common.get_not_found(test_client, path, object_id)

            def test_create_conformation_wrong_payload(
                self, test_client, setup_conformation
            ):
                path, _, _ = setup_conformation
                common.create_wrong_payload(test_client, path)

        class TestWeight:
            def test_create_weight_event(self, test_client, setup_weight):
                path, key, data = setup_weight
                common.create_get(test_client, path, data, key)

            def test_create_delete_weight_event(self, test_client, setup_weight):
                path, key, data = setup_weight
                common.create_delete(test_client, path, data, key)

            def test_get_weight_event_not_found(
                self, test_client, object_id, setup_weight
            ):
                path, _, _ = setup_weight
                common.get_not_found(test_client, path, object_id)

            def test_create_weight_event_wrong_payload(self, test_client, setup_weight):
                path, _, _ = setup_weight
                common.create_wrong_payload(test_client, path)

        class TestGroupWeight:
            def test_create_group_weight_event(self, test_client, setup_group_weight):
                path, key, data = setup_group_weight
                common.create_get(test_client, path, data, key)

            def test_create_delete_group_weight_event(
                self, test_client, setup_group_weight
            ):
                path, key, data = setup_group_weight
                common.create_delete(test_client, path, data, key)

            def test_get_group_weight_event_not_found(
                self, test_client, object_id, setup_group_weight
            ):
                path, _, _ = setup_group_weight
                common.get_not_found(test_client, path, object_id)

            def test_create_group_weight_event_wrong_payload(
                self, test_client, setup_group_weight
            ):
                path, _, _ = setup_group_weight
                common.create_wrong_payload(test_client, path)
