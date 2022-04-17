import os
import pytest
import tempfile

import main


@pytest.fixture
def client():
    file, temp_path = tempfile.mkstemp()
    main._TASKS_DB_FILE_PATH = temp_path
    with main.app.test_client() as client:
        with main.app.app_context():
            main.setup()
        yield client

    os.close(file)
