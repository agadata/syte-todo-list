def test_sanity(client):
    """
    Basic scenario for adding a new task to the list
    """
    title = 'title1'
    content = 'content1'
    response = client.post(f'/add_task?title={title}&content={content}')
    assert response.status_code == 200

    list_string = client.get('/get_list').text
    assert list_string == f'[title: {title}, content: {content}, is done: False]'


def test_missing_content(client):
    """
    Verify failure when trying to add a task without a content
    """
    title = 'title1'
    response = client.post(f'/add_task?title={title}')
    assert response.status_code == 500 and response.text == 'Both title and content parameters must be provided.'


def test_already_exists(client):
    """
    Verify failure when trying to add a task which already exists in the list
    """
    title = 'title1'
    content = 'content1'

    response = client.post(f'/add_task?title={title}&content={content}')
    assert response.status_code == 200

    response = client.post(f'/add_task?title={title}&content={content}')
    assert response.status_code == 500 and response.text == 'Task already exists in the list!'
