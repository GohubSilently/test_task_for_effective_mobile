import uuid

from django.db import models


class User(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)
    email = models.EmailField('Почта', unique=True)
    is_active = models.BooleanField('Активный', default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Session(models.Model):
    session_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
