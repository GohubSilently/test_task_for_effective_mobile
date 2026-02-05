from django.urls import path

from .views import DeleteView, LoginView, RegistrationView, LogoutView, UpdateView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('delete/', DeleteView.as_view()),
    path('update/', UpdateView.as_view())
]