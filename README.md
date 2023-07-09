# Сайт Foodgram "Продуктовый помощник"
> 158.160.20.167

## О проекте
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Используемые технологии
- Python 3.7
- Django 3.2 
- Django REST Framework 3.13.1
- Djoser 2.1.0
- gunicorn 20.0.4
- nginx 1.21.3
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
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "ivan@mail.ru",
            "id": 1,
            "username": "Ivan",
            "first_name": "Иван",
            "last_name": "Иванов",
            "is_subscribed": false
        },
        {
            "email": "nika@mail.ru",
            "id": 3,
            "username": "Nika",
            "first_name": "Nika",
            "last_name": "Nikova",
            "is_subscribed": false
        },
        {
            "email": "puma@mail.ru",
            "id": 2,
            "username": "Puma",
            "first_name": "",
            "last_name": "",
            "is_subscribed": false
        },
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
        "id": 3,
        "name": "Завтрак",
        "color": "#7ab3d0",
        "slug": "breakfast"
    },
    {
        "id": 1,
        "name": "Десерт",
        "color": "#ffc0cb",
        "slug": "dessert"
    },
    {
        "id": 2,
        "name": "Ужин",
        "color": "#b01030",
        "slug": "dinner"
    },
    {
        "id": 5,
        "name": "Напиток",
        "color": "#1919e6",
        "slug": "drink"
    },
    {
        "id": 4,
        "name": "Суп",
        "color": "#d2691e",
        "slug": "soup"
    }
]
```
==============================

> Автором проекта является начинающий backend-разработчик
> 
> Запесочный Владислав.
> 
> Страница на github: https://github.com/SpeZzz0R  
> 
