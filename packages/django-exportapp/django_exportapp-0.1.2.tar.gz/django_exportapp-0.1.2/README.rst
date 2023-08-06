=====
django_exportapp
=====

django_exportapp is a simple Django app to export models xml fixtures.

Quick start
-----------
1. Install django-exportapp::

    pip install django-exportapp

2. Add "django-exportapp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'django_exportapp',
    )

3. Add add variables to settings project like this::

    EXPORTAPP_PUBLIC_DIR = '/home/user/dpub'
    EXPORTAPP_PRIVATE_DIR = '/home/user/private'
