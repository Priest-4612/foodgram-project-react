# **FOODGRAM | Продуктовый помощник**
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
=== [Полная документация к API](http://51.250.97.183/api/docs/) ===  
=== [Панель администратора](http://51.250.97.183/admin/) ===
## **Описание**

Посетить веб-сайт проекта ---> [51.250.97.183](http://51.250.97.183)

Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других авторов, добавлять понравившиеся рецепты в Избранное, а перед походом в магазин скачивать список ингредиентов для понравившихся блюд. Ресурсы FOODGRAM:

+ [Ресурс AUTH](http://51.250.97.183/api/v1/auth/): аутентификация.
+ [Ресурс USERS](http://51.250.97.183/api/v1/users/): пользователи.
+ [Ресурс SUBSCRIPTIONS](http://51.250.97.183/api/v1/users/subscriptions/): пользователи, на которых подписан текущий пользователь.
+ [Ресурс RECIPES](http://51.250.97.183/api/v1/recipes/): рецепты, которые можно добавить в Избранное или список покупок.
+ [Ресурс INGREDIENTS](http://51.250.97.183/api/v1/ingredients/): список ингредиентов к блюдам с возможностью поиска по имени.
+ [Ресурс TAGS](http://51.250.97.183/api/v1/tags/): списк тегов к блюдам.
+ [Ресурс FAVORITES](http://51.250.97.183/api/v1/recipes/favorites/): добавление/удаление рецепта из списка Избранного.
+ [Ресурс SHOPPING CART](http://51.250.97.183/api/v1/recipes/shopping_cart/): добавление/удаление рецепта из списка покупок.
+ [Ресурс DOWNLOAD SHOPPING CART](http://51.250.97.183/api/v1/recipes/download_shopping_cart/): скачать список покупок.

**Стек технологий:**
* Python
* Django REST Framework
* Docker
* Nginx
* React
* Git

Для тестирования функциональности проекта воспользуйтесь следующими данными для входа:
- E-mail: vpupkin@e-pochta.ru
- Пароль: 987Qwerty123

### Установка
1. Войдите в папку infra
2. Создайте файл .env c следующими параметрами:

- Пример:
```
- APP_KEY='c38fd9e9130bb60a65ba0018bbd26a27c7d48f4a' # секретный ключ
- APP_DEBUG=true # статус разработки
- APP_URL=51.250.97.183 # адрес приложения

- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_HOST=db  # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД
- POSTGRES_DB=foodgram # имя базы данных
- POSTGRES_USER='DB_USERNAME' # логин для подключения к базе данных
- POSTGRES_PASSWORD='DB_PASSWORD' # пароль для подключения к БД (установите свой)

- PGADMIN_DEFAULT_EMAIL='test@test.ru'
- PGADMIN_DEFAULT_PASSWORD='test'
- PGADMIN_CONFIG_SERVER_MODE='False'
```
3. Запустите docker-compose командой ```docker-compose up```. У вас развернётся проект, запущенный через Gunicorn с базой данных Postgres.

5. Выполните по очереди команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
6. Проверьте работоспособность приложения:
- зайдите на http://51.250.97.183/admin/ и убедитесь, что страница отображается полностью: статика подгрузилась;
- авторизуйтесь под аккаунтом суперпользователя и убедитесь, что миграции прошли успешно;
- протестируйте приложение, например, через Postman.

### Автор
- Автор: Кричевцов Антон.
- Когорта: 18
- Репозиторий гит: https://github.com/Priest-4612/foodgram-project-react
