## Foodgram - отличный сервис для любителей покушать.

URL: http://geckoyaproject.ddns.net
Login: admin@support.com
Pass: verystr000ngpass!

##### Возможности сервиса:

- Создание, просмотр, редактирование и удаление рецептов.
- Добавление рецептов в избранное.
- Формирование списка покупок.

#### Развертывание проекта локально:

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

5. Измените server_name в файле nginx.conf на ваш домен.

6. Запустите проект:

    ```bash
    sudo docker compose -f docker-compose.yml up
    ```

7. Выполните миграции:

    ```bash
    sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
    ```

8. Соберите статические файлы бэкенда:

    ```bash
    sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
    ```

9. Создайте суперпользователя:

    ```bash
    sudo docker exec -it foodgram-back python manage.py createsuperuser
    ```

10. Загрузите данные в базу (опционально):

    ```bash
    sudo docker exec -it foodgram-back python manage.py load_elements_from_json --file_path ./data_for_load/ingredients.json --model_name Ingredient --app_name recipes
    ```

    ```bash
    sudo docker exec -it foodgram-back python manage.py load_elements_from_json --file_path ./data_for_load/tags.json --model_name Tag --app_name recipes
    ```

11. Можно приступать к наполнению сайта рецептами!


#### Деплой проекта на удаленном сервере:

1. Файл workflow уже написан. Рекомендуется внимательно изучить содержимое. Файл находится в директории:

    ```bash
    foodgram-project-react/.github/workflows/main.yml
    ```

2. В GitHub Actions необходимо добавить следующие секреты (для полей БД можно взять в качестве образца файл /foodgram-project-react/for_devs/env.dev):

    ```bash
    DOCKER_USERNAME                # имя пользователя в DockerHub
    DOCKER_PASSWORD                # пароль пользователя в DockerHub

    HOST                           # ip_address сервера
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

    TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
    TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
    ```

3. Опционально: измените данные для создания суперпользователя в скрипте deploy_data в директории foodgram/infra удаленного сервера и запустите его. Он запустит миграции, наполнит БД стартовыми данными, создаст суперпользователя:


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


### Технология

API разработан: Леонид Цыбульский
