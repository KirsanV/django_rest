from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон", help_text="Укажите номер телефона")
    city = models.CharField(max_length=50, blank=True, verbose_name="Город", help_text="Укажите город")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар", help_text="Загрузите аватар")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('bank_transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь',
        help_text='Пользователь, совершивший платеж'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты',
        help_text='Дата и время совершения платежа'
    )
    course = models.ForeignKey(
        'lms.Course',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Курс',
        help_text='Курс, за который произведена оплата'
    )
    lesson = models.ForeignKey(
        'lms.Lesson',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Урок',
        help_text='Урок, за который произведена оплата'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты',
        help_text='Размер платежа в валюте'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты',
        help_text='Метод оплаты (наличные, перевод и т.д.)'
    )

    def __str__(self):
        return f"Платеж {self.id} от {self.user.email} на сумму {self.amount} ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']