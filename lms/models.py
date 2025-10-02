from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Укажите название курса")
    preview = models.ImageField(upload_to="lms/course_previews/", verbose_name="Превью курса", help_text="Загрузите превью курса", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса", help_text="Укажите описание курса")

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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name