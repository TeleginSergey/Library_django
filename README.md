# Library_django insruction

## Attention!
## Some commands can be diffirent depending on your OS and distributions
## This instruction was written for Linux Ubuntu


## Dependency installation
Intsall different python's frameworks and libraries on your computer (will be better if you will use venv)
```
pip install -r requirements.txt
```
Also you must download django through your package manager,
for example at Linux Ubuntu:
```
sudo apt install django
```

## Using venv (virtual enviroment)
Creating venv:
```
python -m venv <name_of_your_venv>
```
Activating venv:
```
source <name_of_your_venv>/bin/activate
```


## Launching a web application.
Additionally, to run this web application, you need to create a ".env" file and insert the following information:

```
PG_HOST=localhost
PG_PORT=5435
PG_USER=app
PG_PASSWORD=123
PG_DBNAME=library_db
SECRET_KEY='django-insecure-5fw#p!7adj=f8d178!w)qggy63q!+j2x^(b#uu62^5_c3iy9h_'
MINIO_ACCESS_KEY_ID=user
MINIO_SECRET_ACCESS_KEY=password
MINIO_STORAGE_BUCKET_NAME=static
MINIO_API=http://127.0.0.1:9000
```

Also you need to create a docker container for database:
```
docker run -d --name library -p 5435:5432 -e POSTGRES_USER=app -e POSTGRES_PASSWORD=123 -e POSTGRES_DB=library_db postgres
```

After it, with this command
```
psql -h localhost -p 5435 -U app library_db
```
you will get into open-source relational database management system, there write:
```
create schema library;
```
"\q" for quit.

after it you can write this commands:

* python3 manage.py makemigrations
* python3 manage.py migrate
* python3 manage.py runserver

Congratulations!!!

You can launch it later by simply typing the command:
- python3 manage.py runserver



## Launching tests command
- python3 manage.py test tests

Attention! If the tests are not passing, try renaming the folder "tests" to a different name, for example "testing". Accordingly, you will also need to change name "tests" in settings.py.

## Superuser
To enter the admin panel ('admin/'), you need to create a superuser. Here is the command for creating one:
- python3 manage.py createsuperuser

## Minio
MinIO is an open-source distributed object storage server compatible with Amazon S3. It is typically used for storing large amounts of unstructured data like images, videos, backups, logs, and container images.
Start docker container for MinIO:
```
docker run -d --name minio_3 -p 9000:9000 -p 9001:9001 -e "MINIO_ROOT_USER=user" -e "MINIO_ROOT_PASSWORD=password" minio/minio server /data --console-ad
```
If you go to the address in the browser https://127.0.0.1:9001 and register (login, password are provided in the command below, which you should enter), you will be able to create a storage. Our application expects a storage of type public, as well as a directory "static", where, accordingly, there will be PDF files for reading on our web application.

## Problems

### Logout
if you can't log out of your account on this web-app,
insert at templates/base_generic.html instead logout (delete whe whole 16 line) this code:
```
<form method="post" action="{% url 'logout' %}?next={{request.path}}">
    {% csrf_token %}
    <input type="submit" value="Logout">
</form>
```

Thanks for reading:)