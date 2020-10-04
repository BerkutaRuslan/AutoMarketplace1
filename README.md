## General info
AutoMarketplace API made with Django Rest Framework

## Docs
https://documenter.getpostman.com/view/12856650/TVKFyvSx

## Technologies
Project is created with:
* Python v3.8
* Django v3.1
* Django Rest Framework v3.11.1
* psycopg2-binary v2.8.5
* PostgreSQL v11

### How to run a project
Activate virtualenv: (venv - your virtual environment name)
```shell script
$ source venv/bin/activate
```

To start server got to the project root and run:
```shell script
$ python3 manage.py runserver
```

To make and apply migrations run the following command:
```shell script
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py loaddata initial_data.json
```

