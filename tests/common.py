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
            assert response[k] == payload[k]
        except AssertionError as e:
            # Handle inaccurate date matching - ignore
            if is_date(str(response[k])) or is_date(str(payload[k])):
                return
            # Handle nested dicts
            if isinstance(response[k], dict) or isinstance(payload[k], dict):
                check_object_similarity(payload[k], response[k])
            else:
                raise e


def create_get(test_client, path, payload, key):
    response = test_client.post(path, json=payload)
    response_json = response.json()
    assert response.status_code == 201
    response = test_client.get(
        path + f"/?ft={response_json['ft']}")
    assert response.status_code == 200
    assert len(response.json()[key]) == 1
    response_json = response.json()[key][0]
    check_object_similarity(payload, response_json)
