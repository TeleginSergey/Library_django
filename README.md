# Library_django

# Launching a web application (write in terminal).
* python3 manage.py makemigrations
* python4 manage.py migrate
* python3 manage.py runserver

# Launching tests
- python3 manage.py test tests

Attention! If the tests are not passing, try renaming the folder "tests" to a different name. Accordingly, you will also need to change name "tests" in settings.py.

# Superuser
To enter the admin panel ('admin/'), you need to create a superuser. Here is the command for creating one:
- python3 manage.py createsuperuser

Thanks for reading