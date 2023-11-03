Микросервис по отправке email:
- RestAPI позволяет создовать запись уведомления в документе пользователя
- БД MongoDB
- отправка email через smtp сервер mail.ru
- документация swwager (в кастомных методах нет описания параметров, нужно в методах добавить описание для swwager)
- предоставляет листинг уведомлений пользователя
- максимальное количество уведомлений для пользователя 10 (более старые удаляються)
- если нет пользователя, при создании уведомления необходимо передать параметр email вместо user_id, это создаст ново пользователя и создаст запись.
- автоматическое создание user_id из 24 символов
- переменные окружения храняться в .env файле который находиться рядом с settings.py



endpoints:
- api/ (страница с доступными моделями)
- api/users/ (все пользователи)
- api/users/user_id/ (получить выбранного пользователя)
- api/notifications/ (все уведомления)
- api/create/ (POST запрос создание уведомления params: user_id[string]: Не обязательно, key[string]: Обязательно, target_id[string]: Не обязательно, data: {'key': 'value'} Не обязательно, можно передать email[string] вместо user_id для создания нового пользователя и уведомления для него, 
параметр key отвечает за действие с уведомлением 
      - registration (Только отправит пользователю Email)
      - new_message (только создаст запись в документе пользователя)
      - new_post (только создаст запись в документе пользователя)
      - new_login (Создаст запись в документе пользователя и отправит email))
- api/read/ (POST запрос Изменить статус уведомления как прочитанное params: user_id: [string] Обязательный, notification_id: [string] Обязательный)
- api/list/?user_id=[string]&skip=[int]&limit=[int] (GET запрос, user_id обязательный параметр, limit(к-во) и skip(к-во пропустить уведомлений) не обязательные)
- api/docs/ (Документация swwager)

Пред сборкой создайте .env фаил рядом с settings.py:
"""
EMAIL=dima_protasevich92@mail.ru
PASSWORD=x7V4VKpEbLJZDW3reb5J
EMAIL_PORT=465 # 2525
EMAIL_HOST=smtp.mail.ru
DEFAULT_FROM_EMAIL=dima_protasevich92@mail.ru

ENGINE=djongo
NAME_DB=mydatabase
HOST=mongodb://mongodb:27017
USERNAME=root
PASSWORD_DB=password
AUTH_SOURCE=admin
AUTH_MECHANISM=SCRAM-SHA-1
"""

Сборка проекта:
'''docker-compos build'''
Запуск проекта:
'''docker-compose up'''
Выпонение миграций в контейнере:
'''docker exec -it id-контейнера python manage.py migrate'''

API:
"""http://127.0.0.1:8000/api/"""
"""http://localhost:8000/api/"""



