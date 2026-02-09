from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mock/', include('mock.urls')),
    path('api/', include('api.urls')),
]
