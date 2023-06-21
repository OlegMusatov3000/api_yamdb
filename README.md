 <p align="center">
   <img src="https://github.com/yandere410/README/blob/main/Screenshot%20from%202023-06-22%2001-05-39.png?raw=true" title="yamdb"alt="yamdbapi"/>

<h1 class="inlineElement"  32px; letter-spacing: -0.02em;  color: rgb(15, 184, 206 align="center");">Проект YAMDB  предоставляет API для работы с произведениями.</h1>

<h2 align="center"> Установка и настройка </h2>
<p><h3>Клонируйте репозиторий проекта с GitHub:</h3></p>
<div><h3>https://github.com/OlegMusatov3000/api_yamdb</h3></div>
<p>Перейдите в каталог проекта:</p>

cd /api_yamdb

Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate

Установите зависимости:
pip install -r requirements.txt

Выполните миграции базы данных:
python manage.py migrate

Запустите сервер разработки:

python manage.py runserver
API будет доступно по адресу http://localhost:8000/api/v1/.

<h3>Использование</h3>

API позволяет фильтровать записи модели Title по различным параметрам.
Откройте инструмент для работы с API, такой как Postman или curl.
Отправьте GET-запрос по адресу http://localhost:8000/api/v1/titles/ для получения всех записей модели Title.
Используйте параметры запроса для фильтрации результатов. Доступные параметры:

name: фильтрация по названию.
year: фильтрация по году.
genre: фильтрация по жанру (используется поле slug жанра).
category: фильтрация по категории (используется поле slug категории).

Пример запроса с фильтром по названию:
GET /api/v1/titles/?name=example
Получите отфильтрованные результаты в формате JSON.

<h2>Вклад</h2>
Если вы хотите внести свой вклад в проект YAMDB API, вы можете сделать следующее:

Создайте форк репозитория.
Внесите необходимые изменения.
Отправьте запрос на объединение изменений.
Мы будем рады рассмотреть ваши предложения и принять вклад в проект. 

<h2>Сделано при помощи </h2>

<img src="https://github.com/yandere410/README/blob/main/Untitled.png?raw=true">
