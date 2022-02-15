from django.urls import path
from .views import RegisterPage, LoginPage, LogoutPage

urlpatterns = [
    path('register', RegisterPage, name='registerpage'),
    path('login', LoginPage, name='loginpage'),
    path('logout', LogoutPage, name='logoutpage')
]