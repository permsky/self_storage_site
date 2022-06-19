# SelfStorage

Сайт склада вещей для физических и юридических лиц. Можно, например, арендовать ячейку для хранения сезонных вещей или мебели во время переезда.

## Запуск

Для запуска в системе должен быть установлен Python 3.

- Скачайте код
- Создайте и активируйте виртуальное окружение командой:
```bash
python -m venv env && source env/bin/activate
```
- Установите зависимости командой:
```bash
pip install -r requirements.txt
```
- Создайте в корне проекта файл `.env` с переменными окружения:

  <pre>
  SECRET_KEY=*секретный ключ проекта, например `erofheronoirenfoernfx49389f43xf3984xf9384`*
  DEBUG=*дебаг-режим. Поставьте `True`, чтобы увидеть отладочную информацию в случае ошибки. Выключается значением `False`*
  EMAIL_HOST=*адрес smtp-сервера например `smtp.gmail.com`*
  EMAIL_PORT=*порт smtp-сервера*
  EMAIL_USE_TLS=True
  EMAIL_HOST_USER=*email, с которого будет отправляться письмо пользователю после регистрации*
  EMAIL_HOST_PASSWORD=*пароль приложения, генерируется в настройках почтового аккаунта* 
  </pre>
- Создайте базу данных и примените миграции командами:
```bash
python manage.py makemigrations storage_manager
python manage.py migrate
```
- Создайте учётную запись администратора командой:
```bash
python manage.py createsuperuser
```
- Запустите сервер командой:
```bash
python manage.py runserver
```
- Загрузите начальные данные о складах в базу данных командой:
```bash
python manage.py load_from_json
```

После этого главная страница будет доступна по адресу [127.0.0.1:8000](http://127.0.0.1:8000), админка — [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- Запустите dramatiq-воркеры командой:
```bash
python manage.py rundramatiq
```
- Запустите планировщик APScheduler командой:
```bash
python manage.py run_scheduler
```
После данных действий активируется процесс отправки email-оповещений клиентам сервиса SelfStorage. 

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
