# Weather App

## Описание

Приложение Weather App предназначено для отображения данных о погоде по городам. Оно позволяет пользователям искать погоду в различных городах, просматривать историю запросов, получать статистику по наиболее часто искомым городам и использовать автозаполнение при вводе названия города.

## Установка и настройка

### Требования

- Python 3.12
- PostgreSQL
- Docker
- Docker Compose

### Установка (с использованием Docker)

1. **Клонируйте репозиторий:**

    ```bash
    git clone git@github.com:HodzukimaruU/WetherProject.git
    cd WeatherProject
    ```

2. ***Создайте файл `.env` на одну папку выше корневой и добавьте в него следующие переменные окружения:**

    ```.env
    SECRET_KEY=<ваш_django_ключ>
    DEBUG_MODE=True
    DB_NAME=weather_db
    DB_HOST=db
    DB_PORT=5432
    DB_USER=<ваш пользователь>
    DB_PASSWORD=<ваш пороль>

    Так же создан env.template. В нем так же хранится то что нужно добавить в .env
    ```

3. **Запустите контейнеры Docker:**

    ```bash
    docker-compose up --build
    ```

4. **Примените миграции:**

    В новом окне терминала запустите:

    ```bash
    docker-compose exec web python WeatherProject/manage.py migrate
    ```

5. **Создайте суперпользователя (опционально):**

    ```bash
    docker-compose exec web python WeatherProject/manage.py createsuperuser
    ```

6. **Откройте приложение в браузере:**

    Перейдите по адресу [http://localhost:8000](http://localhost:8000).

### Установка (без использования Docker)

1. **Клонируйте репозиторий:**

    ```bash
    git clone git@github.com:HodzukimaruU/WetherProject.git
    cd WeatherProject
    ```

2. **Создайте и активируйте виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Создайте файл `.env` на одну папку выше корневой и добавьте в него следующие переменные окружения:**

    ```.env
    SECRET_KEY=<ваш_django_ключ>
    DEBUG_MODE=True
    DB_NAME=weather_db
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=<ваш пользователь>
    DB_PASSWORD=<ваш пороль>

    Так же создан env.template. В нем так же хранится то что нужно добавить в .env
    ```

5. **Настройте базу данных PostgreSQL:**

    Создайте базу данных и пользователя PostgreSQL.

    ```Подключение к PostgreSQL как суперпользователь
    psql -U postgres
    ```

    ```sql
    CREATE DATABASE weather_db;
    CREATE USER <ваш пользователь> WITH PASSWORD '<ваш пороль>';
    GRANT ALL PRIVILEGES ON DATABASE weather_db TO <ваш пользователь>;
    ```

6. **Зайдите в директорию с файлом manage.py и примените миграции:**

    ```bash
    python3 manage.py migrate
    ```

7. **Создайте суперпользователя (опционально):**

    ```bash
    python3 manage.py createsuperuser
    ```

8. **Запустите сервер разработки:**

    ```bash
    python3 manage.py runserver
    ```

9. **Откройте приложение в браузере:**

    Перейдите по адресу [http://localhost:8000](http://localhost:8000).

## Структура проекта
- **WeatherProject/**
   - **weather/**: Основное приложение Django.
     - **migrations/**: Миграции базы данных.
     - **templates/**: Шаблоны HTML.
     - **__init__.py**: Инициализация приложения.
     - **admin.py**: Настройки админки.
     - **apps.py**: Конфигурация приложения.
     - **forms.py**: Формы для ввода данных.
     - **models.py**: Модели данных.
     - **tests.py**: Тесты для приложения.
     - **urls.py**: URL-ы приложения.
     - **views.py**: Представления для обработки запросов.
   - **WeatherProject/**: Основной проект Django.
     - **__init__.py**: Инициализация проекта.
     - **asgi.py**: ASGI-конфигурация.
     - **settings.py**: Настройки проекта.
     - **urls.py**: Главные URL-ы проекта.
     - **wsgi.py**: WSGI-конфигурация.
   - **.env**
   - **manage.py**
- **.env.template**: Пример того что нужно в .env файле.
- **Dockerfile**: Инструкция для создания Docker-образа.
- **docker-compose.yaml**: Конфигурация Docker Compose.
- **requirements.txt**: Список зависимостей Python.
- **README.md**

## Использование

### Основные функции

- **Поиск погоды:** Введите название города в форму на главной странице для получения прогноза погоды.
- **История запросов:** Перейдите на страницу истории, чтобы просмотреть список всех предыдущих запросов.
- **Автозаполнение:** При вводе названия города вы получите предложения на основе предыдущих запросов.
- **Статистика городов:** Посмотрите, какие города искались чаще всего.
- **Повторный поиск:** Перейдите по ссылке для повторного поиска погоды для определенного города.

### Примечания
- Понимаю что в docker-compose сейчас есть build. Понимаю, что для продашена это неправильно.
- Я сейчас залью как есть. И сейчас же начну исправлять, чтобы было как для продашена.

### API

- **https://api.opencagedata.com/**: Используется во views в get_coordinates для получения координат.
- **https://api.open-meteo.com/**: Используется во views в get_weather_data для получения погоды.

## Тестирование

1. **Для запуска тестов используйте команду (Если используете Docker)**: 

    ```bash
    docker-compose exec web python WeatherProject/manage.py test
    ```

2. **Для запуска тестов используйте команду (Если запускать через python3)**: 

    ```bash
    python3 manage.py test
    ```

### Лицензия

**MIT License**
