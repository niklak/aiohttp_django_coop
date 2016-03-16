# Angularjs application that uses Django Rest Framework and Aiohttp

Actually it is a Django application with Angularjs application stored in Django`s static root.
Angularjs app. uses DRF app. for user authentication and retreiving channel list and chat history.
For real-time messaging this app. uses aiohttp web-server with one web-socket handler.


### Django REST Framework app. requires:
1. Django 1.9
1. djangorestframework 3.3.2
1. psycopg2 2.6.1
1. django-debug-toolbar (optionally, for the debug)
1. redis (optionally)
1. django-redis-cache (optionally)

### Aiohttp app. requires:
1. aiohttp 0.21.2
1. aioredis 0.2.5
1. aiopg 0.9.2

#### Angularjs app. uses cdn packages (1.5.0) 

