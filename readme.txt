setup & start API server:
1. install flask (pip install flask)
2. add flask.exe to PATH
3. from the project root, run: flask run

usage:
- add task:
	[POST] http://127.0.0.1:5000/add_task?title=title1&content=content1
  tasks are identified by their title, so there can't be two tasks with the same title in the list
- remove task:
	[POST] http://127.0.0.1:5000/remove_task?title=task1
- mark task as done:
	[POST] http://127.0.0.1:5000/mark_task_as_done?title=task1
- get list:
	[GET] http://127.0.0.1:5000/get_list

to run the tests, install pytest library and run the following command from the project root:
python -m pytest
