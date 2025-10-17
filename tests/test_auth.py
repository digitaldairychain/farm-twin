
import pytest
from .common import get_access_token_header


class TestAuth:

    @pytest.mark.order('first')
    def test_registration_success(self, test_client, setup_registration):
        user = setup_registration
        response = test_client.post('/users/user', json=user)
        response_json = response.json()
        assert response.status_code == 201
        del user["password"]  # Password not returned in response
        assert response_json == user

    @pytest.mark.order(1)
    def test_registration_invalid(self, test_client, setup_user):
        user = setup_user
        del user["password"]  # Remove password from registration user
        response = test_client.post('/users/user', json=user)
        assert response.status_code == 422

    @pytest.mark.order(1)
    def test_duplicate_registration(self, test_client, setup_user):
        user = setup_user
        response = test_client.post('/users/user', json=user)
        assert response.status_code == 404

    @pytest.mark.order(2)
    def test_fetch_token(self, fetch_token):
        response = fetch_token
        assert response.status_code == 200
        response_json = response.json()
        assert "access_token" in response_json
        assert "bearer" in response_json["token_type"]

    @pytest.mark.order(3)
    def test_get_disabled_user(self, fetch_token, test_client):
        header = get_access_token_header(fetch_token)
        response = test_client.get('users/user', headers=header)
        assert response.status_code == 400

    @pytest.mark.order(4)
    def test_get_user(self, setup_registration, fetch_token, enable_user_in_db, test_client):
        enable_user_in_db
        header = get_access_token_header(fetch_token)
        user = setup_registration
        response = test_client.get('users/user', headers=header)
        response_json = response.json()
        assert response.status_code == 200
        del user["password"]  # Password not returned in response
        assert response_json == user

    @pytest.mark.order('last')
    def test_remove_user(self, fetch_token, test_client):
        header = get_access_token_header(fetch_token)
        del_response = test_client.delete(
            '/users/user', headers=header)
        assert del_response.status_code == 200
        get_response = test_client.get('/users/user', headers=header)
        assert get_response.status_code == 404

    # TODO: get outside scope
    # TODO: unauthorised access
