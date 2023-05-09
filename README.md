![foodgram-project-react workflow](https://github.com/SpeZzz0R/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


# Сайт Foodgram "Продуктовый помощник"

## О проекте
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Используемые технологии
- Python 3.7
- Django 3.2 
- Django REST Framework 3.13.1
- Djoser 2.1.0
- gunicorn 20.0.4
- nginx 1.21.1
- PostgreSQL 15.0

## Запуск проекта
* Клонируйте репозиторий.
```
git@github.com:SpeZzz0R/foodgram-project-react.git
```
* Перейдите в его корневую папку
* Создайте виртуальное окружение Python версии 3.7. Активируйте его
```
py -3.7 -m venv venv
. venv/Scripts/activate
```
* Перейдите в папку backend, в которой находится файл requirements.txt
* Установите зависимости из файла requirements.txt и обновите пакет pip
```
cd backend
pip install -r requirements.txt
python -m pip install --upgrade pip
```
* Перейдите в папку infra, в которой находится файл docker-compose.yaml
* Создайте контейнер
```
cd ..
cd infra_server
```
* Переименуйте файд .to-env в .env
* Создайте контейнеры.
```
docker-compose up
```

## Примеры запросов

#### GET /api/users/ 
```
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "dima@mail.ru",
            "id": 2,
            "username": "Dima",
            "first_name": "Dima",
            "last_name": "Dimov",
            "is_subscribed": false
        },
        {
            "email": "james@mail.ru",
            "id": 1,
            "username": "James",
            "first_name": "James",
            "last_name": "Jamison",
            "is_subscribed": false
        },
        {
            "email": "maria@mail.ru",
            "id": 3,
            "username": "Maria",
            "first_name": "Мария",
            "last_name": "Петрова",
            "is_subscribed": false
        },
        {
            "email": "nika@mail.ru",
            "id": 4,
            "username": "Nika",
            "first_name": "Ника",
            "last_name": "Никова",
            "is_subscribed": false
        },
        {
            "email": "puma@mail.ru",
            "id": 5,
            "username": "Puma",
            "first_name": "",
            "last_name": "",
            "is_subscribed": false
        },
        {
            "email": "sergei@mail.ru",
            "id": 6,
            "username": "Sergei",
            "first_name": "Сергей",
            "last_name": "Сергеев",
            "is_subscribed": false
        }
    ]
}
```

#### POST /api/users/ 
```
{
    "password": [
        "Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.",
        "Введённый пароль слишком широко распространён.",
        "Введённый пароль состоит только из цифр."
    ]
}
```

#### GET /api/tags/
```
[
    {
        "id": 2,
        "name": "Борщ",
        "color": "#734a12",
        "slug": "borsch"
    },
    {
        "id": 1,
        "name": "Жар. картошка",
        "color": "#ffd700",
        "slug": "fried_fri"
    }
]
```
==============================

> Автором проекта является начинающий backend-разработчик
> Запесочный Владислав. 
> Страница на github: https://github.com/SpeZzz0R  
> 
