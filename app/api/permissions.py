from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from users.models import Action, Permission, Resource


def check_permissions(user, resource, action):
    if user.role.name == 'admin':
        return True
    try:
        resource = Resource.objects.get(name=resource)
        action = Action.objects.get(name=action)
    except (Resource.DoesNotExist, Action.DoesNotExist):
        return False
    return Permission.objects.filter(
        role=user.role,
        resource=resource,
        action=action
    ).exists()


class CustomPermission:
    resource = None
    actions = {
        'GET': 'get',
        'POST': 'post',
        'PUT': 'put',
        'PATCH': 'patch',
        'DELETE': 'delete',
    }

    def check(self, request):
        if not request.user:
            raise NotAuthenticated('Пользователь не аутентифицирован')

        action = self.actions.get(request.method)
        if not action:
            raise PermissionDenied('Недопустимое действие')

        if not check_permissions(
            user=request.user,
            resource=self.resource,
            action=action
        ):
            raise PermissionDenied('Недостаточно прав')
