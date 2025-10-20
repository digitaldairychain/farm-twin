import pytest


class TestAuth:
    @pytest.mark.order("first")
    def test_registration_success(self, test_client, setup_registration):
        user = setup_registration
        response = test_client.post("/users/user", json=user)
        response_json = response.json()
        assert response.status_code == 201
        del user["password"]  # Password not returned in response
        assert response_json == user

    @pytest.mark.order(1)
    def test_registration_invalid(self, test_client, setup_user):
        user = setup_user
        del user["password"]  # Remove password from registration user
        response = test_client.post("/users/user", json=user)
        assert response.status_code == 422

    @pytest.mark.order(1)
    def test_duplicate_registration(self, test_client, setup_user):
        user = setup_user
        response = test_client.post("/users/user", json=user)
        assert response.status_code == 404

    @pytest.mark.order(2)
    def test_fetch_token_user(self, fetch_token_user):
        _, token, status_code = fetch_token_user
        assert status_code == 200
        assert "access_token" in token
        assert "bearer" in token["token_type"]

    @pytest.mark.order(3)
    def test_get_disabled_user(self, fetch_token_user, test_client):
        header, _, _ = fetch_token_user
        response = test_client.get("users/user", headers=header)
        assert response.status_code == 400

    @pytest.mark.order(4)
    def test_get_user(
        self, setup_registration, fetch_token_user, enable_user_in_db, test_client
    ):
        enable_user_in_db
        header, _, _ = fetch_token_user
        user = setup_registration
        response = test_client.get("users/user", headers=header)
        response_json = response.json()
        assert response.status_code == 200
        del user["password"]  # Password not returned in response
        assert response_json == user

    @pytest.mark.order(5)
    def test_outside_scope(self, fetch_token_user, test_client, set_admin_in_db):
        header, _, _ = fetch_token_user
        response = test_client.get("objects/animals", headers=header)
        assert response.status_code == 401
        set_admin_in_db  # Set as admin for future tests

    @pytest.mark.order("last")
    def test_remove_user(self, fetch_token_admin, test_client):
        header, _, _ = fetch_token_admin
        del_response = test_client.delete("/users/user", headers=header)
        assert del_response.status_code == 200
        get_response = test_client.get("/users/user", headers=header)
        assert get_response.status_code == 404
