from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@shared_task
def ping_user(user_id):
    return f"Pinged user {user_id}"

@shared_task
def deactivate_inactive_users(days=30):
    User = get_user_model()
    cutoff = timezone.now() - timedelta(days=days)
    updated_count = User.objects.filter(is_active=True, last_login__lt=cutoff).update(is_active=False)
    return f"Deactivated {updated_count} user(s) inactive since {cutoff}"