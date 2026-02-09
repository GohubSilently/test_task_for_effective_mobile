from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import Session


class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Анонимному пользователю доступ запрещен!')
        if not auth_header.startswith('Session '):
            raise AuthenticationFailed('Неверный заголовок, должен быть "Session"')

        token = auth_header.replace('Session ', '')
        try:
            session = Session.objects.select_related('user').get(session_token=token)
        except Session.DoesNotExist:
            raise AuthenticationFailed('Данная сессия не найдена!')

        user = session.user
        if user.is_active is False:
            raise AuthenticationFailed('Ваш аккаунт удален!')

        return user, session
