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

### Запуск проекта

```bash
docker-compose up --build