set -e

python manage.py migrate
python manage.py migrate django_celery_beat || true

celery -A config worker -l info &

celery -A config beat -l info