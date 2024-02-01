## Foodgram - отличный сервис для любителей покушать.

##### Возможности сервиса:

- Создание, просмотр, редактирование и удаление рецептов.
- Добавление рецептов в избранное.
- Формирование списка покупок.

#### Развертывание проекта локально (для разработки):

1. Установите Docker и Docker-compose. Запустите сервис Docker.

2. Склонируйте репозиторий на свой компьютер:

    ```bash
    git clone git@github.com:CuriousGecko/foodgram-project-react.git
    ```

    ```bash
    cd foodgram-project-react/for_devs/
    ```

3. Наполните файл env.dev своими данными.

4. Перейдите в директорию:

    ```bash
    cd ../infra/
    ```

5. Запустите проект:

    ```bash
    sudo docker compose -f docker-compose-local.yml up
    ```

6. Выполните миграции:

    ```bash
    sudo docker exec foodgram-back python manage.py migrate
    ```

7. Соберите статические файлы бэкенда:

    ```bash
    sudo docker exec foodgram-back python manage.py collectstatic
    ```

8. Создайте суперпользователя:

    ```bash
    sudo docker exec -it foodgram-back python manage.py createsuperuser
    ```

9. Загрузите данные в базу (опционально):

    ```bash
    sudo docker exec foodgram-back python manage.py load_elements_from_json --file_path ./data_for_load/ingredients.json --model_name Ingredient --app_name ingredients
    ```

    ```bash
    sudo docker exec foodgram-back python manage.py load_elements_from_json --file_path ./data_for_load/tags.json --model_name Tag --app_name tags
    ```


#### Автоматический деплой проекта на удаленном сервере:

1. Файл workflow уже написан. Рекомендуется внимательно изучить содержимое. Файл находится в директории:

    ```bash
    foodgram-project-react/.github/workflows/main.yml
    ```

2. В GitHub Actions необходимо добавить следующие секреты (для полей БД можно взять в качестве образца файл /foodgram-project-react/for_devs/env.dev):

    ```bash
    DOCKER_USERNAME                # имя пользователя в DockerHub
    DOCKER_PASSWORD                # пароль пользователя в DockerHub

    HOST                           # IP-адрес сервера
    USER                           # имя пользователя
    SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
    SSH_PASSPHRASE                 # кодовая фраза (пароль) для ssh-ключа
    
    DB_ENGINE                      # какой движок будет использовать Django для БД
    DB_USER                        # пользователь БД
    DB_PASSWORD                    # пароль пользователя БД
    DB_NAME                        # название БД
    DB_HOST                        # к какому контейнеру подключаемся
    DB_PORT                        # порт БД
    POSTGRES_USER                  # == DB_USER
    POSTGRES_PASSWORD              # == DB_PASSWORD
    POSTGRES_DB                    # == DB_NAME
   
    SERVER_NAME                    # домен вашего проекта и\или IP-адрес сервера
    NGINX_EXTERNAL_PORT            # какой внешний порт будет слушать контейнер Nginx

    TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
    TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
    ```

3. Опционально: измените данные для создания суперпользователя в скрипте deploy_data.sh в директории foodgram/infra удаленного сервера и запустите его. Будут применены миграции, БД наполнится стартовыми данными, создастся суперпользователь.


### Запросы к API

Теперь вы можете отправлять запросы к api, например, создать пользователя. Пример POST-запроса к api/users/:

```
{
    "email": "user@mail.com",
    "username": "user",
    "password": "user_password",
    "first_name": "user_first_name",
    "last_name": "user_last_name"
}
```

Вся документация по API доступна по адресу api/docs/redoc.html


### Технология
Проект разработан на базе Django REST framework, аутентификация настроена с помощью Djoser + SimpleJWT.
Полный список библиотек в файле backend/requirements.txt.

API разработан: Леонид Цыбульский
