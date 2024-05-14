# SOKOL-SHOP
#### Сайт магазина страйкбольного оборудования SOKOL

#### 4 основных модуля: товары, корзина, информация о компании, пользователи

После деплоя тестовая версия доступа на http://www.l93774vs.beget.tech/

### Локальный запуск с Docker compose
- Рядом с файлом manage.py разместить .env файл. Env переменные:
```  
EMAIL_HOST='mailhog'
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=1025
DEFAULT_FROM_EMAIL='sokolairsoftshop-test-no-reply@outlook.com'
MANAGER_EMAIL='sokolairsoftshop-test@outlook.com'
SECRET_KEY='some_secret_key'
DB_ENGINE='mysql.connector.django'
DB_NAME='sokol_db'
DB_USER='myuser'
DB_PASSWORD='mypassword'
DB_HOST='db'
DB_PORT=3306
EMAIL_USE_TLS='False'
ALLOWED_HOSTS = '127.0.0.1 localhost www.l93774vs.beget.tech l93774vs.beget.tech'
DEBUG='False'
```
- В основной папке для создания образа
```console  
docker compose build web
```
- Выполнить команду для миграций
```console  
docker compose run --rm web python manage.py migrate
``` 
- Запустить проект
```console  
docker compose up
```
- Для отображения статических файлов через nginx при DEBUG = False
```console  
docker-compose exec web python manage.py collectstatic --no-input 
```

Сайт отобразится по адресу http://127.0.0.1:5000/

### Запуск тестов
- Для запуска всех тестов  
```console  
docker compose run --rm web python manage.py test --settings=sokol.settings_test
```