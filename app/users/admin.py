from django.contrib import admin

from .models import Role, User, Action, Permission, Resource, Session

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Action)
admin.site.register(Resource)
admin.site.register(Session)
