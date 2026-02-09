from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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

documantation_router = [
    path('schema/', SpectacularAPIView.as_view(authentication_classes=[]), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(authentication_classes=[]), name='docs'),
]

urlpatterns = [
    path('auth/', include(auth_router)),
    path('docs/', include(documantation_router)),
    path('profile/', include(profile_router)),
    path('', include(router.urls))
]
