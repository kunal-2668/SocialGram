from django.urls import path
from .views import *

app_name = 'AuthApp'

urlpatterns = [
    path("signup",SignupView,name='signup'),
    path("login",LoginView,name='login'),
    path('logout',LogoutView,name='logout')
]