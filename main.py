import os
from flask import Flask, request, Response
from sqlite3 import connect, register_adapter, register_converter, PARSE_DECLTYPES

_TASKS_DB_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasks.db')
_TASKS_TABLE_NAME = 'tasks'

app = Flask(__name__)


def _table_exists():
    """
    Checks whether the tasks table exists in the db or not
    :return: True if the tasks table exists in the db, False otherwise
    """
    with connect(_TASKS_DB_FILE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{_TASKS_TABLE_NAME}'; ''')
        result = cursor.fetchone()[0] == 1

    connection.close()
    return result


def _create_table():
    """
    Creates the tasks table in the db
    """
    with connect(_TASKS_DB_FILE_PATH, detect_types=PARSE_DECLTYPES) as connection:
        connection.execute(f'''CREATE TABLE {_TASKS_TABLE_NAME}
                 (TITLE     TEXT        PRIMARY KEY        NOT NULL,
                 CONTENT    TEXT,
                 IS_DONE    BOOLEAN                        NOT NULL);
        ''')

    connection.close()


def _task_record_exists(title):
    """
    Checks whether the given task record exists in the table, by its title
    :param title: Title of the task to check its existence in the table
    :return: True if the task record exists in the table, False otherwise
    """
    with connect(_TASKS_DB_FILE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(f'''SELECT count(*) FROM {_TASKS_TABLE_NAME} WHERE TITLE = '{title}';''')
        result = cursor.fetchone()[0] == 1

    connection.close()
    return result


def _insert_task_record(title, content):
    """
    Inserts a new task record to the table
    :param title: Title of the task record
    :param content: Content of the task record
    """
    with connect(_TASKS_DB_FILE_PATH, detect_types=PARSE_DECLTYPES) as connection:
        register_adapter(bool, int)
        register_converter("BOOLEAN", lambda v: bool(int(v)))
        cursor = connection.cursor()
        cursor.execute(f'''INSERT INTO {_TASKS_TABLE_NAME} (TITLE, CONTENT, IS_DONE) \
                           VALUES (?,?,?);''', (title, content, False))

    connection.close()


def _delete_task_record(title):
    """
    Deletes an existing task record form the table
    :param title: Title of the task record to be deleted
    """
    with connect(_TASKS_DB_FILE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(f'''DELETE FROM {_TASKS_TABLE_NAME} \
                           WHERE TITLE = '{title}';''')

    connection.close()


def _get_task_status(title):
    """
    Checks the status (done / not done) of a task record
    :param title: Title of the task whose status should be checked
    :return: True if the task is done, False otherwise
    """
    with connect(_TASKS_DB_FILE_PATH, detect_types=PARSE_DECLTYPES) as connection:
        register_adapter(bool, int)
        register_converter("BOOLEAN", lambda v: bool(int(v)))
        cursor = connection.cursor()
        cursor.execute(f'''SELECT IS_DONE FROM {_TASKS_TABLE_NAME} WHERE TITLE = '{title}';''')
        result = cursor.fetchone()[0]

    connection.close()
    return result


def _mark_record_as_done(title):
    """
    Updates the record of a given task to set its status as done
    :param title: Title of the task record whose status should be updated
    """
    with connect(_TASKS_DB_FILE_PATH, detect_types=PARSE_DECLTYPES) as connection:
        register_adapter(bool, int)
        register_converter("BOOLEAN", lambda v: bool(int(v)))
        cursor = connection.cursor()
        cursor.execute(f'''UPDATE {_TASKS_TABLE_NAME} set IS_DONE = (?) where TITLE = '{title}';''', (True,))

    connection.close()


def _get_all_records():
    """
    :return: All task records in the tasks table
    """
    with connect(_TASKS_DB_FILE_PATH, detect_types=PARSE_DECLTYPES) as connection:
        register_adapter(bool, int)
        register_converter("BOOLEAN", lambda v: bool(int(v)))
        cursor = connection.cursor()
        cursor.execute(f'''SELECT TITLE, CONTENT, IS_DONE FROM {_TASKS_TABLE_NAME};''')
        records = [row for row in cursor]

    connection.close()
    return records


def setup():
    """
    Runs preliminary setup actions, which currently includes creating the tasks table in the db if it doesn't exist
    """
    if not _table_exists():
        _create_table()


@app.route('/add_task', methods=['POST'])
def add_task():
    """
    Adds a new task to the list
    """
    title = request.args.get('title', None)
    content = request.args.get('content', None)
    if not title or not content:
        return Response(status=500, response='Both title and content parameters must be provided.')

    if _task_record_exists(title):
        return Response(status=500, response='Task already exists in the list!')

    _insert_task_record(title, content)
    return Response(status=200)


@app.route('/remove_task', methods=['POST'])
def remove_task():
    """
    Removes an existing task from the list
    """
    title = request.args.get('title', None)
    if not title:
        return Response(status=500, response='Title parameter must be provided')

    if not _task_record_exists(title):
        return Response(status=500, response='Task does not exist in the list')

    _delete_task_record(title)
    return Response(status=200)


@app.route('/mark_task_as_done', methods=['POST'])
def mark_task_as_done():
    """
    Changes the status of a given task to be considered as "Done"
    """
    title = request.args.get('title', None)
    if not title:
        return Response(status=500, response='Title parameter must be provided')

    if not _task_record_exists(title):
        return Response(status=500, response='Task does not exist in the list')

    if _get_task_status(title):
        return Response(status=500, response='The given task has already been marked as done')

    _mark_record_as_done(title)
    return Response(status=200)


@app.route('/get_list', methods=['GET'])
def get_list():
    """
    :return: All tasks in the list, along with their status
    """
    records = _get_all_records()
    record_delimiter = '<br/>'
    return f"[{record_delimiter.join([f'title: {record[0]}, content: {record[1]}, is done: {record[2]}' for record in records])}]"


setup()
