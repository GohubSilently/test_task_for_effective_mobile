# Тестовое задание для Effective Mobile


## Установка
1. Клонируем репозиторий.
```
git clone 
cd test_task_for_effective_mobile
```

2. Создаем .env
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgress_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY='your_secret_key'
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
```

3. Загружаем данные.
```bash
python manage.py migrate
python manage.py load_action && python manage.py load_role && python manage.py load_resource && python manage.py load_permission
python manage.py load_user && python manage.py load_session
python manage.py runserver
```

4. Открываем документацию API - [ссылка](http://127.0.0.1:8000/api/docs/swagger/)



### P.S. Как я пришел к данной реализации. Если интересно почитать.
1. Когда я прочитал тз, я начал искать информацию, про аутентификацию и авторизацию.
Сначала прочитал, статью на Хабре, как работает 'django.contrib.auth'. - [ссылка](https://habr.com/ru/companies/otus/articles/855086/)
После этого наткнулся на видос, который длится около двух часов (спасибо за возможности ускорить видео). - [ссылка](https://www.youtube.com/watch?v=7jnJbZIvQ5s)
С помощью видео я повторил основы, и наткнулся на новые интересные алгоритмы по хешированию паролей. (bcrypt, argon2)
P.S. Почитал про них, и наткнулся на библиотеку для Python.
2. При просмотре этого видео, я уже впринципе решил для себя, что буду использовать сессии, а именно токены, не JWT.
Если честно, не вижу проблемы переделать под JWT, дело 20 минут.
Однако, с библтотекой JWT я уже работал раньше, и решил попробовать что-то новое для себя.
3. Изначально по коммитам в ветку можно понять насколько код претерпел изменения.
Честно, я дольше пытался придумать как назвать проект, чем сколько заняла его реализация.
В тз написано, рекомендация база PostgreSQL, изначально я запустил ее в Docker, так что оставил файл на всякий случай в репозитории.

