import uuid
import bcrypt

from django.db import models


class BaseModel(models.Model):
    name = models.CharField('Название')
    description = models.CharField('Описание')


class Role(BaseModel, models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return f'{self.name} - {self.description}'


class Action(BaseModel, models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = 'HTTP метод'
        verbose_name_plural = 'HTTP методы'

    def __str__(self):
        return f'{self.name} - {self.description}'


class Resource(BaseModel, models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):
        return f'{self.name} - {self.description}'



class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)

    class Meta:
        ordering = ('resource',)
        verbose_name = 'Право'
        verbose_name_plural = 'Права'

    def __str__(self):
        return f'{self.resource} - {self.action} - {self.role}'


class User(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)
    email = models.EmailField('Почта', unique=True)
    password = models.CharField('Пароль', max_length=63)  # Длина ограничена библиотекой
    is_active = models.BooleanField('Активный', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=1)

    class Meta:
        ordering = ('is_active',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email} - {self.role} - {self.is_active}'

    def set_password(self, password):
        hashed_passwords = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_passwords.decode('utf-8')

    def check_password(self, password):
        return True if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')) else False


class Session(models.Model):
    session_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def __str__(self):
        return f'{self.user.email} - {self.session_token}'
