from django.urls import include, path
from rest_framework import routers

from .views import (
    ChangePermissionViewSet, DeleteView, LoginView, LogoutView,
    RegistrationView, UpdateView
)

router = routers.DefaultRouter()
router.register('change_permissions', ChangePermissionViewSet)

auth_router = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]

profile_router = [
    path('update/', UpdateView.as_view()),
    path('delete/', DeleteView.as_view())
]

urlpatterns = [
    path('auth/', include(auth_router)),
    path('profile/', include(profile_router)),
    path('', include(router.urls))
]