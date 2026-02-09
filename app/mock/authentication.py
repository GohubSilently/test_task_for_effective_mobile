from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MockUser:
    def __init__(self, role_name: str):
        self.is_authenticated = True
        self.is_active = True
        self.role = type("Role", (), {"name": role_name})


class MockAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            raise AuthenticationFailed("Анонимному пользователю доступ запрещен!")

        if not token.startswith("Session "):
            raise AuthenticationFailed('Неверный заголовок, должен быть "Session"')

        role = token.replace("Session ", "")

        if role not in ("admin", "moderator", "user"):
            raise AuthenticationFailed("Данная сессия не найдена!")

        return MockUser(role), None
