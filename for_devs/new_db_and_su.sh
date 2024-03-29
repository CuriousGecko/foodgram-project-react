#!/bin/bash

cd ../backend

source ./venv/bin/activate &&

rm db.sqlite3
rm django_db

python3.9 manage.py makemigrations &&
python3.9 manage.py migrate &&

python3.9 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user=User.objects.create_superuser(
email='admin@support.com',
username='admin',
first_name='ad',
last_name='min',
password='verystr000ngpass!')
user.save()
" || exit 1

echo -e "\033[92m\n>>> The preparation is complete! <<<\n\033[0m"

python3.9 manage.py runserver
