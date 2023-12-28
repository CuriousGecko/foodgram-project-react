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

3. Наполните файл env.for_dev своими данными.

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
1. Склонируйте репозиторий на свой компьютер:

    ```bash
    git clone git@github.com:CuriousGecko/foodgram-project-react.git
    ```

    ```bash
    cd foodgram-project-react
    ```

2. Создайте образы (замените username на ваш логин на DockerHub):

    ```bash
    cd frontend
    ```

    ```bash
    sudo docker build -t username/foodgram_front .
    ```

    ```bash
    cd ../backend
    ```

    ```bash
    sudo docker build -t username/foodgram_back .
    ```

4. Загрузите образы на DockerHub:

    ```bash
    sudo docker push username/foodgram_front
    ```

    ```bash
    sudo docker push username/foodgram_back
    ```

5. Подключитесь к удаленному серверу

    ```bash
    ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера
    ```

6. Установите Nginx, Docker и Docker-compose. Запустите сервис Docker.

7. Создайте директорию foodgram/infra в домашней директории сервера:

    ```bash
    mkdir kittygram/infra
    ```

8. В директории kittygram/infra создайте файл docker-compose.production.yml со следующим содержимым (замените docker_username на ваш логин на DockerHub):

```yaml
version: '3.3'

volumes:
  pg_data:
  static:
  media:

services:
  db:
    container_name: foodgram-db
    image: postgres:13
    env_file: .env
    volumes:
      - pg_data:/var/lib/postgresql/data

  frontend:
    container_name: foodgram-front
    image: username/foodgram_frontend:latest
    volumes:
      - ./frontend/:/app/result_build/

  backend:
    container_name: foodgram-back
    image: username/foodgram_backend:latest
    env_file: .env
    volumes:
      - static:/app/collected_static/
      - media:/app/media/
    depends_on:
      - db

  nginx:
    container_name: foodgram-gateway
    image: nginx:1.22.1
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./frontend/build:/usr/share/nginx/html/
      - ../docs/:/usr/share/nginx/html/api/docs/
      - static:/var/html/static/
      - media:/var/html/media/
    depends_on:
      - db
      - backend
```

9. В директории foodgram/infra создайте файл .env (в качестве образца используйте env.for_dev из клонированного репозитория).

10. Из директории infra клонированного репозитория скопируйте на сервер в foodgram/infra файл nginx.conf. Измените в нем server_name на ваш домен.

11. Запустите docker compose в режиме демона:

    ```bash
    sudo docker compose -f docker-compose.production.yml up -d
    ```

12. Измените данные для создания суперпользователя в скрипте deploy_data в директории foodgram/infra удаленного сервера и запустите его. Он запустит миграции, наполнит БД стартовыми данными, создаст суперпользователя:

    ```bash
    bash deploy_data
    ```

### Настройка CI/CD

1. Файл workflow уже написан. Он находится в директории

    ```bash
    foodgram-project-react/.github/workflows/main.yml
    ```

2. Для адаптации его на своем сервере добавьте секреты в GitHub Actions:

    ```bash
    DOCKER_USERNAME                # имя пользователя в DockerHub
    DOCKER_PASSWORD                # пароль пользователя в DockerHub

    HOST                           # ip_address сервера
    USER                           # имя пользователя
    SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
    SSH_PASSPHRASE                 # кодовая фраза (пароль) для ssh-ключа

    TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
    TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
    ```

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
