![foodgram-project-react workflow](https://github.com/SpeZzz0R/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Сайт Foodgram "Продуктовый помощник"


## О проекте
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта
* Клонируйте репозиторий.
```
git@github.com:SpeZzz0R/foodgram-project-react.git
```
* Перейдите в его корневую папку.
* Создайте виртуальное окружение Python версии 3.7. Активируйте его.
```
py -3.7 -m venv venv
. venv/Scripts/activate
```
* Перейдите в папку backend, в которой находится файл requirements.txt
* Установите зависимости из файла requirements.txt и обновите пакет pip.
```
cd backend
pip install -r requirements.txt
python -m pip install --upgrade pip
```
* Перейдите в папку infra, в которой находится файл docker-compose.yaml.
* Создайте контейнер.
```
cd ..
cd infra_server
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

==============================

> Над проектом работал:  
>
> Владислав Запесочный https://github.com/SpeZzz0R  
> 
