from django.urls import path
from .views import RegisterPage, LoginPage, LogoutPage, OrdersPage, ProfilePage

urlpatterns = [
    path('register', RegisterPage, name='registerpage'),
    path('login', LoginPage, name='loginpage'),
    path('logout', LogoutPage, name='logoutpage'),
    path('profile/', ProfilePage.as_view(), name='profilepage'),
    path('orders/', OrdersPage.as_view(), name='orderspage')
]