# Django, uWSGI and Nginx in a container

This Dockerfile allows you to build a Docker container with a fairly standard
and speedy setup for Django with uWSGI and Nginx.

### Build and run
* docker build -t webapp .
* docker run -d webapp

### How to insert your application

In /app currently a django project is created with startproject. You will
probably want to replace the content of /app with the root of your django
project, and delete manage.py.

Revise uwsgi.ini :module=*YourDjangoProjectName*.wsgi:application. you will need to make sure the python path
to the wsgi.py file is relative to that.

### Tree
'''
app:
│  requirements.txt
│
└─demo
    │  forms.py
    │  settings.py
    │  tests.py
    │  urls.py
    │  views.py
    │  wsgi.py
    │  __init__.py
    │
    ├─templates
    │  └─demo
    │          base.html
    │          bootstrap.html
    │          form.html
    │          formset.html
    │          form_by_field.html
    │          form_horizontal.html
    │          form_inline.html
    │          form_with_files.html
    │          home.html
    │          misc.html
    │          pagination.html
'''
