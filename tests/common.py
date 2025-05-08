from dateutil.parser import parse


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def check_object_similarity(payload, response):
    """Check response contains at least the payload data."""
    for k in payload.keys():
        try:
            assert payload[k] == response[k]
        except AssertionError as e:
            # Handle inaccurate date matching - ignore
            if is_date(str(response[k])) or is_date(str(payload[k])):
                return
            # Handle nested dicts
            if isinstance(response[k], dict) or isinstance(payload[k], dict):
                check_object_similarity(payload[k], response[k])
            else:
                raise e


def create_get(test_client, path, payload, key, expected_code=201):
    """
    POST an object with a given payload and the GET the contents to check
    if it exists.
    """
    response = test_client.post(path, json=payload)
    response_json = response.json()
    assert response.status_code == expected_code
    if response.status_code == 201:
        response = test_client.get(
            path + f"/?ft={response_json['ft']}")
        assert response.status_code == 200
        assert len(response.json()[key]) == 1
        response_json = response.json()[key][0]
        check_object_similarity(payload, response_json)
        return response_json


def create_get_update(test_client, path, payload, payload_updated, key,
                      expected_code=202):
    """
    POST an object with a given payload, PATCH it with an updated payload, 
    then GET the contents to check if it exists.
    """
    response_json = create_get(test_client, path, payload, key)
    _id = response_json['ft']
    response = test_client.patch(
        path + f"/{_id}",
        json=payload_updated,
    )
    response_json = response.json()
    assert response.status_code == expected_code
    if expected_code == 202:
        check_object_similarity(payload_updated, response_json)


def create_delete(test_client, path, payload, key):
    """
    POST an object with a given payload, DELETE an object with a given payload 
    and then GET the contents to check if it exists (it shouldn't).
    """
    response_json = create_get(test_client, path, payload, key)
    _id = response_json['ft']
    response = test_client.delete(
        path + f"/{_id}")
    assert response.status_code == 204
    response = test_client.get(
        path + f"/?ft={_id}")
    assert response.status_code == 404


def get_not_found(test_client, path, object_id):
    """GET a random object that shouldn't exist."""
    response = test_client.get(
        path + f"/?ft={object_id}")
    assert response.status_code == 404


def create_wrong_payload(test_client, path):
    """POST with an invalid payload"""
    response = test_client.post(path, json={})
    assert response.status_code == 422


def update_doesnt_exist(test_client, path, payload, object_id):
    """PATCH an object that doesn't exist."""
    response = test_client.patch(
        path + f"/{object_id}", json=payload
    )
    assert response.status_code == 404


def create_duplicate(test_client, path, payload, key):
    """POST the same object twice - the second time should produce an error."""
    create_get(test_client, path, payload, key)
    create_get(test_client, path, payload, key, expected_code=404)
