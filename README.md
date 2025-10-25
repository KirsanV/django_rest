# Django LMS Project

Проект системы управления обучением (LMS) на Django с использованием Docker.

## Технологии

- **Backend**: Django, Django REST Framework
- **База данных**: PostgreSQL
- **Асинхронные задачи**: Celery + Redis
- **Платежи**: Stripe
- **Контейнеризация**: Docker, Docker Compose
- **Документация**: автоматическая генерация через DRF

## Быстрый старт

### Предварительные требования

- Файл `.env` с необходимыми переменными окружения (скопируйте из `sample.env`)
# Настройка сервера (Ubuntu)
1. ssh username@your-server-ip
2. sudo apt update && sudo apt upgrade -y
3. sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl
4. sudo ufw allow OpenSSH
5. sudo ufw allow 'Nginx Full'
6. sudo ufw --force enable

# Настройка базы данных
## Создание БД и пользователя
1. sudo -u postgres psql -c "CREATE DATABASE drf;"
2. sudo -u postgres psql -c "CREATE USER myapp_user WITH PASSWORD 'your_password';"
3. sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE drf TO myapp_user;"
## Запуск Redis
1. sudo systemctl enable redis-server
2. sudo systemctl start redis-server

# Развертывание приложения
## Создание директории проекта
1. sudo mkdir -p /var/www/myapp
2. sudo chown $USER:$USER /var/www/myapp
3. cd /var/www/myapp

## Клонирование репозитория
1. git clone https://github.com/KirsanV/django_rest.git .

## Настройка виртуального окружения
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt

## Настройка переменных окружения
1. cp sample.env .env
2. nano .env  # Заполните реальными данными

## Применение миграций и сбор статических файлов
1. python manage.py migrate
2. python manage.py collectstatic --noinput

# Настройка Gunicorn
1. Создайте файл /etc/systemd/system/gunicorn.service

        [Unit]
        Description=gunicorn daemon for Django app
        After=network.target postgresql.service redis-server.service
        
        [Service]
        User=your-username
        Group=www-data
        WorkingDirectory=/var/www/myapp
        ExecStart=/var/www/myapp/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/myapp/myapp.sock config.wsgi:application
        ExecReload=/bin/kill -s HUP $MAINPID
        Restart=on-failure
        
        [Install]
        WantedBy=multi-user.target

2. sudo systemctl daemon-reload
3. sudo systemctl enable gunicorn
4. sudo systemctl start gunicorn

# Настройка Nginx
1. Создайте файл /etc/nginx/sites-available/myapp

        server {
            listen 80;
            server_name your-server-ip;
        
            location = /favicon.ico { access_log off; log_not_found off; }
            
            location /static/ {
                root /var/www/myapp;
            }
        
            location /media/ {
                root /var/www/myapp;
            }
        
            location / {
                include proxy_params;
                proxy_pass http://unix:/var/www/myapp/myapp.sock;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header Host $http_host;
                proxy_redirect off;
            }
        }

2. sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
3. sudo rm -f /etc/nginx/sites-enabled/default
4. sudo nginx -t
5. sudo systemctl restart nginx


# Приложение будет доступно по IP адресу вашего сервера.


### Запуск проекта

```bash
docker-compose up --build