from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(authentication_classes=[]), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(authentication_classes=[])),
    path('api/', include('api.urls')),
]
