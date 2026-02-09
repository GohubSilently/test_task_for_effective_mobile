from rest_framework.exceptions import PermissionDenied, NotAuthenticated


MOCK_MATRIX = {
    "donations": {
        "get": ("admin", "moderator"),
        "post": ("user",),
    }
}


class MockCustomPermission:
    resource = None
    actions = {
        "GET": "get",
        "POST": "post",
        "PUT": "put",
        "PATCH": "patch",
        "DELETE": "delete",
    }

    def check(self, request):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not user or not user.is_authenticated:
            raise NotAuthenticated("Пользователь не аутентифицирован")

        action = self.actions.get(request.method)
        if not action:
            raise PermissionDenied("Недопустимое действие")

        allowed_roles = MOCK_MATRIX.get(self.resource, {}).get(action, ())

        if user.role.name not in allowed_roles:
            raise PermissionDenied("Недостаточно прав")
