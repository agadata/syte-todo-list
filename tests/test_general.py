def test_empty_list_on_startup(client):
    """
    Check the task list is empty when server application starts for the first time
    """
    response = client.get('/get_list')
    assert response.status_code == 200
    assert response.text == '[]'

