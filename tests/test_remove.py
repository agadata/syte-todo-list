def test_sanity(client):
    """
    Basic scenario for removing an existing task from the list
    """
    title = 'title1'
    content = 'content1'

    response = client.post(f'/add_task?title={title}&content={content}')
    assert response.status_code == 200

    response = client.post(f'/remove_task?title={title}')
    assert response.status_code == 200

    list_string = client.get('/get_list').text
    assert list_string == '[]'


def test_remove_task_without_title(client):
    """
    Verify failure when trying to remove a task without sending the title parameter
    """
    response = client.post(f'/remove_task')
    assert response.status_code == 500 and response.text == 'Title parameter must be provided'


def test_remove_non_existing_task(client):
    """
    Verify failure when trying to remove a task that does not exist in the list
    """
    title = 'title1'

    response = client.post(f'/remove_task?title={title}')
    assert response.status_code == 500 and response.text == 'Task does not exist in the list'
