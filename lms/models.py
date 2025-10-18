from django.db import models
from django.contrib.auth import get_user_model


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Укажите название курса")
    preview = models.ImageField(upload_to="lms/course_previews/", verbose_name="Превью курса", help_text="Загрузите превью курса", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса", help_text="Укажите описание курса")
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Владелец",
        default=1
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Курс", help_text="Выберите курс")
    name = models.CharField(max_length=100, verbose_name="Название урока", help_text="Укажите название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока", help_text="Укажите описание урока")
    preview = models.ImageField(upload_to="lms/lesson_previews/", verbose_name="Превью урока", help_text="Загрузите превью урока", blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео", blank=True, null=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Владелец",
        default=1
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_subscriptions',
        verbose_name="Курс",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"

    def __str__(self):
        return f"{self.user} подписан на {self.course}"