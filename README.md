# THINKWIK

## Index

- [THINKWIK](#thinkwik)
  - [Index](#index)
    - [Introduction](#introduction)
    - [Installation](#installation)

### Introduction
- Student and Teacher based assessment task
- User authentication available
- Supports latest version of Python i.e. Python 3.10.3  along with Django 4.1.3 :zap:
- Api endpoind available on default server. :nail_care:

| Plugin | **Version**|
| ------ | ------ |
|  pip   | 22.2.2 |
| Python | 3.10.3 |
| Django | 4.1.3 |
| Postgres | 11.6 |

### Installation

> ##### 1. Clone repository

```sh
git clone https://github.com/deepakkumhar/thinkwik.git
```

> ##### 2. If you not having pip,Django let's install

```sh
sudo easy_install pip
```

> ##### 3. Create certual environment and activate

```sh
pipenv shell
```

> ##### 4. Setup The Project

```sh
pipenv install -r requirements.txt
```


> ##### 5. Create Database Manuanlly in PgAdmin
```sh
CREATE DATABASE <database_name>
```

> ##### 6. Setting up your database details in .env

```sh
DB_NAME=DATABASE_NAME
DB_USER=DATABASE_USER
DB_PASSWORD=DATABASE_PASSWORD
DB_HOST=HOST_NAME
DB_PORT=PORT_NUMBER
```

> ##### 7. Create tables by Django migration

```sh
python manage.py makemigrations

python manage.py migrate
```

> ##### 8. All api will be available @ `http://127.0.0.1:8000/`

```
Like Register api - http://127.0.0.1:8000/register/
```

<br />