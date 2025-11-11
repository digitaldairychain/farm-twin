from . import common

ROOT = "events"


class TestEvents:
    class TestFeeding:
        class TestFeedIntake:
            def test_create_feed_intake_event(
                self, test_client, setup_feed_intake
            ):
                path, header, key, data = setup_feed_intake
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_feed_intake_event(
                self, test_client, setup_feed_intake
            ):
                path, header, key, data = setup_feed_intake
                common.create_delete(test_client, path, header, data, key)

            def test_get_feed_intake_event_not_found(
                self, test_client, object_id, setup_feed_intake
            ):
                path, header, _, _ = setup_feed_intake
                common.get_not_found(test_client, path, header, object_id)

            def test_create_feed_intake_wrong_payload(
                self, test_client, setup_feed_intake
            ):
                path, header, _, _ = setup_feed_intake
                common.create_wrong_payload(test_client, path, header)

    class TestWithdrawal:
        def test_create_withdrawal_event(self, test_client, setup_withdrawal):
            path, header, key, data = setup_withdrawal
            common.create_get(test_client, path, header, data, key)

        def test_create_delete_withdrawal_event(
            self, test_client, setup_withdrawal
        ):
            path, header, key, data = setup_withdrawal
            common.create_delete(test_client, path, header, data, key)

        def test_get_withdrawal_event_not_found(
            self, test_client, object_id, setup_withdrawal
        ):
            path, header, _, _ = setup_withdrawal
            common.get_not_found(test_client, path, header, object_id)

        def test_create_withdrawal_wrong_payload(
            self, test_client, setup_withdrawal
        ):
            path, header, _, _ = setup_withdrawal
            common.create_wrong_payload(test_client, path, header)

    class TestMovement:
        class TestArrival:
            def test_create_arrival_event(self, test_client, setup_arrival):
                path, header, key, data = setup_arrival
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_arrival_event(
                self, test_client, setup_arrival
            ):
                path, header, key, data = setup_arrival
                common.create_delete(test_client, path, header, data, key)

            def test_get_arrival_event_not_found(
                self, test_client, object_id, setup_arrival
            ):
                path, header, _, _ = setup_arrival
                common.get_not_found(test_client, path, header, object_id)

            def test_create_arrival_wrong_payload(
                self, test_client, setup_arrival
            ):
                path, header, _, _ = setup_arrival
                common.create_wrong_payload(test_client, path, header)

        class TestBirth:
            def test_create_birth_event(self, test_client, setup_birth):
                path, header, key, data = setup_birth
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_birth_event(self, test_client, setup_birth):
                path, header, key, data = setup_birth
                common.create_delete(test_client, path, header, data, key)

            def test_get_birth_event_not_found(
                self, test_client, object_id, setup_birth
            ):
                path, header, _, _ = setup_birth
                common.get_not_found(test_client, path, header, object_id)

            def test_create_birth_wrong_payload(
                self, test_client, setup_birth
            ):
                path, header, _, _ = setup_birth
                common.create_wrong_payload(test_client, path, header)

        class TestDeath:
            def test_create_death_event(self, test_client, setup_death):
                path, header, key, data = setup_death
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_death_event(self, test_client, setup_death):
                path, header, key, data = setup_death
                common.create_delete(test_client, path, header, data, key)

            def test_get_death_event_not_found(
                self, test_client, object_id, setup_death
            ):
                path, header, _, _ = setup_death
                common.get_not_found(test_client, path, header, object_id)

            def test_create_death_wrong_payload(
                self, test_client, setup_death
            ):
                path, header, _, _ = setup_death
                common.create_wrong_payload(test_client, path, header)

        class TestDeparture:
            def test_create_departure_event(
                self, test_client, setup_departure
            ):
                path, header, key, data = setup_departure
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_departure_event(
                self, test_client, setup_departure
            ):
                path, header, key, data = setup_departure
                common.create_delete(test_client, path, header, data, key)

            def test_get_departure_event_not_found(
                self, test_client, object_id, setup_departure
            ):
                path, header, _, _ = setup_departure
                common.get_not_found(test_client, path, header, object_id)

            def test_create_departure_wrong_payload(
                self, test_client, setup_departure
            ):
                path, header, _, _ = setup_departure
                common.create_wrong_payload(test_client, path, header)

    class TestMilking:
        class TestLactationStatus:
            def test_create_lactation_status_event(
                self, test_client, setup_lactation_status
            ):
                path, header, key, data = setup_lactation_status
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_lactation_status_event(
                self, test_client, setup_lactation_status
            ):
                path, header, key, data = setup_lactation_status
                common.create_delete(test_client, path, header, data, key)

            def test_get_lactation_status_event_not_found(
                self, test_client, object_id, setup_lactation_status
            ):
                path, header, _, _ = setup_lactation_status
                common.get_not_found(test_client, path, header, object_id)

            def test_create_lactation_status_wrong_payload(
                self, test_client, setup_lactation_status
            ):
                path, header, _, _ = setup_lactation_status
                common.create_wrong_payload(test_client, path, header)

        class TestTestDayResult:
            def test_create_test_day_result_event(
                self, test_client, setup_test_day_result
            ):
                path, header, key, data = setup_test_day_result
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_test_day_result_event(
                self, test_client, setup_test_day_result
            ):
                path, header, key, data = setup_test_day_result
                common.create_delete(test_client, path, header, data, key)

            def test_get_test_day_result_event_not_found(
                self, test_client, object_id, setup_test_day_result
            ):
                path, header, _, _ = setup_test_day_result
                common.get_not_found(test_client, path, header, object_id)

            def test_create_test_day_result_wrong_payload(
                self, test_client, setup_test_day_result
            ):
                path, header, _, _ = setup_test_day_result
                common.create_wrong_payload(test_client, path, header)

        class TestDryingOff:
            def test_create_drying_off_event(
                self, test_client, setup_drying_off
            ):
                path, header, key, data = setup_drying_off
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_drying_off_event(
                self, test_client, setup_drying_off
            ):
                path, header, key, data = setup_drying_off
                common.create_delete(test_client, path, header, data, key)

            def test_get_drying_off_event_not_found(
                self, test_client, object_id, setup_drying_off
            ):
                path, header, _, _ = setup_drying_off
                common.get_not_found(test_client, path, header, object_id)

            def test_create_drying_off_wrong_payload(
                self, test_client, setup_drying_off
            ):
                path, header, _, _ = setup_drying_off
                common.create_wrong_payload(test_client, path, header)

        class TestMilkingVisit:
            def test_create_milking_visit_event(
                self, test_client, setup_milking_visit
            ):
                path, header, key, data = setup_milking_visit
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_milking_visit_event(
                self, test_client, setup_milking_visit
            ):
                path, header, key, data = setup_milking_visit
                common.create_delete(test_client, path, header, data, key)

            def test_get_milking_visit_event_not_found(
                self, test_client, object_id, setup_milking_visit
            ):
                path, header, _, _ = setup_milking_visit
                common.get_not_found(test_client, path, header, object_id)

            def test_create_milking_visit_wrong_payload(
                self, test_client, setup_milking_visit
            ):
                path, header, _, _ = setup_milking_visit
                common.create_wrong_payload(test_client, path, header)

    class TestObservations:
        class TestCarcass:
            def test_create_carcass_event(self, test_client, setup_carcass):
                path, header, key, data = setup_carcass
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_carcass_event(
                self, test_client, setup_carcass
            ):
                path, header, key, data = setup_carcass
                common.create_delete(test_client, path, header, data, key)

            def test_get_carcass_event_not_found(
                self, test_client, object_id, setup_carcass
            ):
                path, header, _, _ = setup_carcass
                common.get_not_found(test_client, path, header, object_id)

            def test_create_carcass_wrong_payload(
                self, test_client, setup_carcass
            ):
                path, header, _, _ = setup_carcass
                common.create_wrong_payload(test_client, path, header)

        class TestHealthStatus:
            def test_create_health_status_event(
                self, test_client, setup_health_status
            ):
                path, header, key, data = setup_health_status
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_health_status_event(
                self, test_client, setup_health_status
            ):
                path, header, key, data = setup_health_status
                common.create_delete(test_client, path, header, data, key)

            def test_get_health_status_event_not_found(
                self, test_client, object_id, setup_health_status
            ):
                path, header, _, _ = setup_health_status
                common.get_not_found(test_client, path, header, object_id)

            def test_create_health_status_wrong_payload(
                self, test_client, setup_health_status
            ):
                path, header, _, _ = setup_health_status
                common.create_wrong_payload(test_client, path, header)

        class TestPositionStatus:
            def test_create_position_event(self, test_client, setup_position):
                path, header, key, data = setup_position
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_position_event(
                self, test_client, setup_position
            ):
                path, header, key, data = setup_position
                common.create_delete(test_client, path, header, data, key)

            def test_get_position_event_not_found(
                self, test_client, object_id, setup_position
            ):
                path, header, _, _ = setup_position
                common.get_not_found(test_client, path, header, object_id)

            def test_create_position_wrong_payload(
                self, test_client, setup_position
            ):
                path, header, _, _ = setup_position
                common.create_wrong_payload(test_client, path, header)

    class TestReproduction:
        class TestReproStatus:
            def test_create_repro_status_event(
                self, test_client, setup_repro_status
            ):
                path, header, key, data = setup_repro_status
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_status_event(
                self, test_client, setup_repro_status
            ):
                path, header, key, data = setup_repro_status
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_status_event_not_found(
                self, test_client, object_id, setup_repro_status
            ):
                path, header, _, _ = setup_repro_status
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_status_wrong_payload(
                self, test_client, setup_repro_status
            ):
                path, header, _, _ = setup_repro_status
                common.create_wrong_payload(test_client, path, header)

        class TestReproDNB:
            def test_create_repro_do_not_breed_event(
                self, test_client, setup_repro_do_not_breed
            ):
                path, header, key, data = setup_repro_do_not_breed
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_do_not_breed_event(
                self, test_client, setup_repro_do_not_breed
            ):
                path, header, key, data = setup_repro_do_not_breed
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_do_not_breed_event_not_found(
                self, test_client, object_id, setup_repro_do_not_breed
            ):
                path, header, _, _ = setup_repro_do_not_breed
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_do_not_breed_wrong_payload(
                self, test_client, setup_repro_do_not_breed
            ):
                path, header, _, _ = setup_repro_do_not_breed
                common.create_wrong_payload(test_client, path, header)

        class TestReproAbortion:
            def test_create_repro_abortion_event(
                self, test_client, setup_repro_abortion
            ):
                path, header, key, data = setup_repro_abortion
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_abortion_event(
                self, test_client, setup_repro_abortion
            ):
                path, header, key, data = setup_repro_abortion
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_abortion_event_not_found(
                self, test_client, object_id, setup_repro_abortion
            ):
                path, header, _, _ = setup_repro_abortion
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_abortion_wrong_payload(
                self, test_client, setup_repro_abortion
            ):
                path, header, _, _ = setup_repro_abortion
                common.create_wrong_payload(test_client, path, header)

        class TestReproHeat:
            def test_create_repro_heat_event(
                self, test_client, setup_repro_heat
            ):
                path, header, key, data = setup_repro_heat
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_heat_event(
                self, test_client, setup_repro_heat
            ):
                path, header, key, data = setup_repro_heat
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_heat_event_not_found(
                self, test_client, object_id, setup_repro_heat
            ):
                path, header, _, _ = setup_repro_heat
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_heat_wrong_payload(
                self, test_client, setup_repro_heat
            ):
                path, header, _, _ = setup_repro_heat
                common.create_wrong_payload(test_client, path, header)

        class TestReproInsemination:
            def test_create_repro_insemination_event(
                self, test_client, setup_repro_insemination
            ):
                path, header, key, data = setup_repro_insemination
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_insemination_event(
                self, test_client, setup_repro_insemination
            ):
                path, header, key, data = setup_repro_insemination
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_insemination_event_not_found(
                self, test_client, object_id, setup_repro_insemination
            ):
                path, header, _, _ = setup_repro_insemination
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_insemination_wrong_payload(
                self, test_client, setup_repro_insemination
            ):
                path, header, _, _ = setup_repro_insemination
                common.create_wrong_payload(test_client, path, header)

        class TestReproMatingRecommendation:
            def test_create_repro_mating_recommendation_event(
                self, test_client, setup_repro_mating_recommendation
            ):
                path, header, key, data = setup_repro_mating_recommendation
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_mating_recommendation_event(
                self, test_client, setup_repro_mating_recommendation
            ):
                path, header, key, data = setup_repro_mating_recommendation
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_mating_recommendation_event_not_found(
                self, test_client, object_id, setup_repro_mating_recommendation
            ):
                path, header, _, _ = setup_repro_mating_recommendation
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_mating_recommendation_wrong_payload(
                self, test_client, setup_repro_mating_recommendation
            ):
                path, header, _, _ = setup_repro_mating_recommendation
                common.create_wrong_payload(test_client, path, header)

        class TestReproParturition:
            def test_create_repro_parturition_event(
                self, test_client, setup_repro_parturition
            ):
                path, header, key, data = setup_repro_parturition
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_repro_parturition_event(
                self, test_client, setup_repro_parturition
            ):
                path, header, key, data = setup_repro_parturition
                common.create_delete(test_client, path, header, data, key)

            def test_get_repro_parturition_event_not_found(
                self, test_client, object_id, setup_repro_parturition
            ):
                path, header, _, _ = setup_repro_parturition
                common.get_not_found(test_client, path, header, object_id)

            def test_create_repro_parturition_wrong_payload(
                self, test_client, setup_repro_parturition
            ):
                path, header, _, _ = setup_repro_parturition
                common.create_wrong_payload(test_client, path, header)

    class TestAttention:
        def test_create_attention_event(self, test_client, setup_attention):
            path, header, key, data = setup_attention
            common.create_get(test_client, path, header, data, key)

        def test_create_delete_attention_event(
            self, test_client, setup_attention
        ):
            path, header, key, data = setup_attention
            common.create_delete(test_client, path, header, data, key)

        def test_get_attention_event_not_found(
            self, test_client, object_id, setup_attention
        ):
            path, header, _, _ = setup_attention
            common.get_not_found(test_client, path, header, object_id)

        def test_create_attention_wrong_payload(
            self, test_client, setup_attention
        ):
            path, header, _, _ = setup_attention
            common.create_wrong_payload(test_client, path, header)

    class TestPerformance:
        class TestConformation:
            def test_create_conformation_event(
                self, test_client, setup_conformation
            ):
                path, header, key, data = setup_conformation
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_conformation_event(
                self, test_client, setup_conformation
            ):
                path, header, key, data = setup_conformation
                common.create_delete(test_client, path, header, data, key)

            def test_get_conformation_event_not_found(
                self, test_client, object_id, setup_conformation
            ):
                path, header, _, _ = setup_conformation
                common.get_not_found(test_client, path, header, object_id)

            def test_create_conformation_wrong_payload(
                self, test_client, setup_conformation
            ):
                path, header, _, _ = setup_conformation
                common.create_wrong_payload(test_client, path, header)

        class TestWeight:
            def test_create_weight_event(self, test_client, setup_weight):
                path, header, key, data = setup_weight
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_weight_event(
                self, test_client, setup_weight
            ):
                path, header, key, data = setup_weight
                common.create_delete(test_client, path, header, data, key)

            def test_get_weight_event_not_found(
                self, test_client, object_id, setup_weight
            ):
                path, header, _, _ = setup_weight
                common.get_not_found(test_client, path, header, object_id)

            def test_create_weight_event_wrong_payload(
                self, test_client, setup_weight
            ):
                path, header, _, _ = setup_weight
                common.create_wrong_payload(test_client, path, header)

        class TestGroupWeight:
            def test_create_group_weight_event(
                self, test_client, setup_group_weight
            ):
                path, header, key, data = setup_group_weight
                common.create_get(test_client, path, header, data, key)

            def test_create_delete_group_weight_event(
                self, test_client, setup_group_weight
            ):
                path, header, key, data = setup_group_weight
                common.create_delete(test_client, path, header, data, key)

            def test_get_group_weight_event_not_found(
                self, test_client, object_id, setup_group_weight
            ):
                path, header, _, _ = setup_group_weight
                common.get_not_found(test_client, path, header, object_id)

            def test_create_group_weight_event_wrong_payload(
                self, test_client, setup_group_weight
            ):
                path, header, _, _ = setup_group_weight
                common.create_wrong_payload(test_client, path, header)
