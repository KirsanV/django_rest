from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription


@shared_task
def sample_task():
    return f"Sample task ran at {datetime.utcnow().isoformat()}"


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return f"Course {course_id} not found."

    subscriptions = Subscription.objects.filter(course=course).select_related("user")
    if not subscriptions.exists():
        return f"No subscribers for course {course_id}"

    subject = f'Обновление материалов курса "{course.name}"'
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL")

    for sub in subscriptions:
        user = sub.user
        if user.email:
            message = (
                f'Здравствуйте! В курсе "{course.name}" произошли изменения. '
                f"Пожалуйста, ознакомьтесь с обновлениями в приложении."
            )
            try:
                send_mail(
                    subject, message, from_email, [user.email], fail_silently=False
                )
            except Exception:
                pass

    return f"Emails sent to {subscriptions.count()} subscribers"
