from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', message='Формат: 8(XXX)XXX-XX-XX')],
        verbose_name='Телефон'
    )

    def __str__(self):
        return self.fio


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('under_review', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    title = models.CharField(max_length=200, verbose_name='Название')
    event_date = models.DateField(verbose_name='Желаемая дата')
    category = models.CharField(max_length=100, verbose_name='Категория')
    format = models.CharField(max_length=100, verbose_name='Формат')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to='application_images/', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return self.title