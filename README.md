# Weather App

## Описание

Приложение Weather App предназначено для отображения данных о погоде по городам. Оно позволяет пользователям искать погоду в различных городах, просматривать историю запросов, получать статистику по наиболее часто искомым городам и использовать автозаполнение при вводе названия города.

## Установка и настройка

### Требования

- Docker
- Docker Compose

### Установка (с использованием Docker)

1. Создайте docker-compose.yaml

```yaml

version: '3.9'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: weather_db
      POSTGRES_USER: uppa
      POSTGRES_PASSWORD: < DB_PASSWORD >
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    image: uppa3/djangoweather:1.0.1
    restart: unless-stopped
    ports:
      - "80:8000"
    depends_on:
      - db
    environment:
      - SECRET_KEY='< YOUR_DJANGO_KEY >'
      - DEBUG_MODE=True
      - DB_NAME=weather_db
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=uppa
      - DB_PASSWORD=< DB_PASSWORD >

volumes:
  postgres_data:

```

Запустите:

```shell
docker-compose up -d
```

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

- **Поиск погоды**
- **История запросов**
- **Автозаполнение**
- **Статистика городов**
- **Повторный поиск**

### API

- **https://api.opencagedata.com/**: Используется во views в get_coordinates для получения координат.
- **https://api.open-meteo.com/**: Используется во views в get_weather_data для получения погоды.

### Лицензия

**MIT License**
