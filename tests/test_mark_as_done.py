def test_sanity(client):
    """
    Basic scenario for marking a task in the list as done
    """
    title = 'title1'
    content = 'content1'

    response = client.post(f'/add_task?title={title}&content={content}')
    assert response.status_code == 200

    response = client.post(f'/mark_task_as_done?title={title}')
    assert response.status_code == 200

    list_string = client.get('/get_list').text
    assert list_string == f'[title: {title}, content: {content}, is done: True]'


def test_no_title(client):
    """
    Verify failure when trying to mark a task as done without specifying a title parameter
    """
    response = client.post(f'/mark_task_as_done')
    assert response.status_code == 500 and response.text == 'Title parameter must be provided'


def test_task_not_exists(client):
    """
    Verify failure when trying to mark a task that does not exist on the list as done
    """
    title = 'title1'

    response = client.post(f'/mark_task_as_done?title={title}')
    assert response.status_code == 500 and response.text == 'Task does not exist in the list'


def test_already_done(client):
    """
    Verify failure when trying to mark a task that has already been marked as done
    """
    title = 'title1'
    content = 'content1'

    response = client.post(f'/add_task?title={title}&content={content}')
    assert response.status_code == 200

    response = client.post(f'/mark_task_as_done?title={title}')
    assert response.status_code == 200

    response = client.post(f'/mark_task_as_done?title={title}')
    assert response.status_code == 500 and response.text == 'The given task has already been marked as done'
