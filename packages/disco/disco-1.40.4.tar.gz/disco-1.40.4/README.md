Dis.co Python SDK
====================
[![Coverage Status](https://coveralls.io/repos/github/Iqoqo/python-sdk/badge.svg?t=c9UU6U)](https://coveralls.io/github/Iqoqo/python-sdk)

This package lets you run jobs on [Dis.co](https://www.dis.co/) platform from a Python program.

Using the SDK, you can create computing jobs, run them on _Dis.co_, and get their results to your local machine. 
It is possible to offload any kind of Python program to be run on _Dis.co_.

Prerequisites
-------------

1. An [Dis.co](https://www.dis.co/) account.
2. Python version 3.6 and up.
3. Dis.co Python SDK installed:

    ```bash
    $ pip install disco
    ```

Example
-------

```python
import disco
import pathlib

disco.set_credentials('john@example.com', 'my_password', save_to_config=True)

my_file_id = disco.upload_file('my_file.py', pathlib.Path('/home/bob/my_file.py'))
job = disco.Job.create(my_file_id)
job.start()

(task_result,) = job.get_results(block=True)
task_result.write_files('/home/bob/my_result')
```

The code above uploads the file `/home/bob/my_file.py`, runs it on _Dis.co_ cloud, waits for the job to finish, 
and writes the results to `/home/bob/my_result`.

When the job has been created, you can see it listed in `list_jobs()`:

```python
>>> import disco
>>> disco.Job.list_jobs())
[{'id': '5d650d25179854000d72b8cc', 'archived': False, 'name': 'd08e3e029bfc412ebc316e21f1a7dae0', 'status': 'Done', 'taskStates': ['Success']}]
```

This functions returns an instance of `Job`, which gives access to many useful operations on a job 
(see the API documentation). 

Environment variables
---------------------

The `disco` package supports these environment variables:

 - `DISCO_BASE_URL` - base URL of the Dis.co server. Default: `https://app.dis.co`
 - `DISCO_EMAIL` - user's email to for authenticating with the Dis.co server.
 - `DISCO_PASSWORD` - password for authenticating with the Dis.co server.
 - `DISCO_LIVE_TESTS` - set true to run our live tests.