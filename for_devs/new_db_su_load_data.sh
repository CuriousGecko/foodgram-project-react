#!/bin/bash

cd ../backend

source ./venv/bin/activate &&

rm django_db

python manage.py collectstatic --no-input

python manage.py makemigrations &&
python manage.py migrate &&

python manage.py load_elements_from_json --file_path ./data_for_load/ingredients.json --model_name Ingredient --app_name ingredients &&

python manage.py load_elements_from_json --file_path ./data_for_load/tags.json --model_name Tag --app_name tags &&

python manage.py shell -c "
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

echo "Суперпользователь успешно создан!"

echo -e "\033[92m\n>>> The preparation is complete! <<<\n\033[0m"
