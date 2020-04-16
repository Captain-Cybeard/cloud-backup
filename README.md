# Cloud Backup Application

####Making a Python Virtual Environment:

`$ python -m venv <name of environment>` (I used cloud-backup-env)

Then add the folder it created to your .gitignore file

`$ source <name of env folder>/bin/activate`

You are now in the virtual environment anything you install will not be system wide

The first time you start:

`$ pip install -r requirements.txt`

To leave the environment:

`$ deactivate`

To add dependencies that you installed please do:

`$ pip freeze > requirements.txt`

Then commit the new requirements.txt to the repo.

#### Running the webserver:
Viewing on the same pc

`$ python manage.py runserver`

Then visit: https://localhost:8000

Viewable from any pc on the network:

`$ python manage.py runserver 0:8000`
