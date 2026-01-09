# api_final
api final

## Описание проекта.

YaTube - это проект в формате блога, в котором пользователи могут писать посты, комментировать свои или чужие посты, подписываться на других пользователей. Данный проект является Rest API для YaTube.

## Установка API YaTube.

Необходимо клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:GalinaLody/api-final-yatube.git
```
```
cd api-final-yatube
```
Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Примеры запросов к API YaTube.

Запросы к API YaTube могут быть отправлены на следующие эндпоинты:
* http://127.0.0.1:8000/api/v1/posts/
* http://127.0.0.1:8000/api/v1/posts/{id}/
* http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
* http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/
* http://127.0.0.1:8000/api/v1/groups/
* http://127.0.0.1:8000/api/v1/groups/{id}/
* http://127.0.0.1:8000/api/v1/follow/

Для просмотра публикаций, комментарий и сообществ регистрации не требуется. ДЛя осуществления иных действий, например, создание, изменение, просмотр подписок требуется аутентификация пользователя.

Для аутентификации и получения токена пользователю необходимо направить запрос на эндпоинт http://127.0.0.1:8000/api/v1/jwt/create/

Пример запроса:
```
{
  "username": "string",
  "password": "string"
}
```
Для содания создание публикации необходимо направит запрос на эндпоинт http://127.0.0.1:8000/api/v1/posts/

Пример запроса:
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
Для пдписки на пользователя необходимо направить запрос на эндпоинт http://127.0.0.1:8000/api/v1/follow/

Пример запроса:
```
{
  "following": "string"
}
```
