# Cloud Backup Application
Language:       Python 3.8 Django 2.2

Dev Env:         Linux x64

Authors:          Ryan Breitenfeldt,
                        Noah Farris,
                        Trevor Surface,
                        Kyle Thomas
                        
Class:              CptS 421/423 Fall 2019/Spring 2020

University:    Washington State University Tri-CIties

### Development

#### Making a Python Virtual Environment:

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

Then visit: https://localhost:8000/cloud

Viewable from any pc on the network:

`$ python manage.py runserver 0:8000`

#### Adding a Cloud Platform
Add the file with the new cloud platform class into `cloud_download/platforms`

Then import the file in `cloud_download/platforms/__init__.py`

Finally, add the platform inside `cloud_download/views.py`
