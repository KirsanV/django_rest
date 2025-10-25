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
7. 
# Развертывание приложения
## Создание директории проекта
1. sudo mkdir -p /var/www/myapp - создание директории на ВМ и переход в нее
2. sudo chown $USER:$USER /var/www/myapp - создание директории на ВМ и переход в нее
3. cd /var/www/myapp - создание директории на ВМ и переход в нее

## Клонирование репозитория
1. git clone https://github.com/KirsanV/django_rest.git .
2. git checkout hm_final - переход в ветку
3. nano .env - вставляем свои данные sample.env
4. nano docker-compose.yaml - измените на свои значения из .env

        postgres:
          image: postgres:15
          environment:
            POSTGRES_USER: #User
            POSTGRES_PASSWORD: #password
            POSTGRES_DB: #name

5. docker compose up -d  - развертка
6. docker compose ps - проверка статусов сервисов
7. docker compose logs --tail=10 django - проверка работы сервиса django
8. curl -I http://localhost - проверка хоста

# Приложение будет доступно по IP адресу.
1. 51.250.16.96


### Запуск проекта

```bash
docker-compose up --build