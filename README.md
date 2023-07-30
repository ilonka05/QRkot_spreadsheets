## Приложение для Благотворительного фонда поддержки котиков QRKot.


### Описание проекта:

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Приложение обслуживает следующие эндпоинты:
|Эндпоинт|Типы запросов|Реализованные функции|
|:----------------------------|:----------|:-------------------------------------------------------------------|
|/charity_project/            |GET, POST  |Получение списка всех проектов; Создание благотворительного проекта.|
|/charity_project/{project_id}|DEL, PATCH |Удаление проекта; Редактирование проекта.                           |
|/donation/                   |GET, POST  |Получение списка всех пожертвований; Выполнить пожертвование.       |
|/donation/my                 |GET        |Получение списка пожертвований пользователя, выполняющего запрос.   |
|/auth/jwt/login              |POST       |Вход пользователя в систему.                                        |
|/auth/jwt/logout             |POST       |Выход пользователя из системы.                                      |
|/auth/register               |POST       |Регистрация пользователя.                                           |
|/users/me                    |GET, PATCH |Получение и изменение информации аутентифицированного пользователя. |
|/users/{id}                  |GET, PATCH |Получение и изменение информации о пользователе по его ID.          |
|/google                      |GET       |Получение отчёта о закрытых проектах в гугл-таблице.                |


### Используемые технологии и библиотеки:
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* [SQLAlchemy](https://docs.sqlalchemy.org/en/14/)
* [Pydantic](https://docs.pydantic.dev/latest/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [Aiogoogle](https://aiogoogle.readthedocs.io/en/latest/#)
* [Google Sheets](https://www.google.ru/intl/ru/sheets/about/)


### Как запустить проект:

- Клонируйте репозиторий на локальную машину

```
git clone git@github.com:ilonka05/QRkot_spreadsheets.git
```

- Перейдите в папку с проектом

```
cd QRkot_spreadsheets
```

- Создайте и активируйте виртуальное окружение

```
python -m venv venv
source venv/Scripts/activate
```

- Обновите pip и установите зависимости из requirements.txt

```
pip install --upgrade pip
pip install -r requirements.txt
```

- В корневой папке проекта создайте файл .env, пример содержания файла:

```
APP_TITLE=Кошачий благотворительный фонд 
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=user@example.com
FIRST_SUPERUSER_PASSWORD=user

# Данные с JSON-файла с ключом доступа к сервисному аккаунту
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
EMAIL=

```

- Примените миграции

```
alembic upgrade head
```

- Запустите проект локально и перейдите по указанной в терминале ссылке

```
uvicorn app.main:app --reload
```

- Ссылки для открытия документации

* http://127.0.0.1:8000/docs
* http://127.0.0.1:8000/redoc

### Авторы проекта:

    Петина Илона
