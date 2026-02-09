from django.urls import path
from .views import DonationMockView

urlpatterns = [
    path("donations/", DonationMockView.as_view()),
]
