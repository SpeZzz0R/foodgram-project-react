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
* Переименуйте файд .to-env в env
* Создайте контейнер.
```
docker-compose up
```
* Проведите миграции, создайте суперпользователя, соберите статику.
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
* Создайте резервную копию базы.
```
docker-compose exec web python manage.py dumpdata > fixtures.json 
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
            "email": "bublik@mail.ru",
            "id": 2,
            "username": "Bublik",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": false
        },
        {
            "email": "dimon@mail.ru",
            "id": 5,
            "username": "Dimon",
            "first_name": "Dimon",
            "last_name": "Dmitriev",
            "is_subscribed": false
        },
        {
            "email": "maria@mail.ru",
            "id": 4,
            "username": "Maria",
            "first_name": "Maria",
            "last_name": "Ivanova",
            "is_subscribed": false
        },
        {
            "email": "j23.2020@yandex.ru",
            "id": 6,
            "username": "NJackson",
            "first_name": "Jack",
            "last_name": "Black",
            "is_subscribed": false
        },
        {
            "email": "vlad.z.spezzz@gmail.com",
            "id": 3,
            "username": "Spez",
            "first_name": "",
            "last_name": "",
            "is_subscribed": false
        },
        {
            "email": "vlad.z.lebron@gmail.com",
            "id": 1,
            "username": "Vladislav",
            "first_name": "",
            "last_name": "",
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

==============================

> Над проектом работал:  
>
> Владислав Запесочный https://github.com/SpeZzz0R  
> 
