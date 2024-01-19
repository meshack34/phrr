# urls.py
from django.urls import path
from .views import HomeView
from .views import RegistrationSerializer
urlpatterns = [
    path('api/home/', HomeView.as_view(), name='home-api'),
    path('register/', views.RegistrationSerializer, name='registration-api'),
]
