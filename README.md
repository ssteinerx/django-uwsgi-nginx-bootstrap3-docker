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
