def test_liveliness(test_client):
    response = test_client.get("/version/")
    assert response.status_code == 200
