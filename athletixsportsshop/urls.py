"""athletixsportsshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import HomePage, CartPage, WishlistPage, CheckoutPage, PlaceOrder, paymenthandler, \
    Faqs, Aboutus, Help, Terms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='homepage'),
    path('account/', include('account.urls')),
    path('store/', include('store.urls')),
    path('cart/', CartPage.as_view(), name='cartpage'),
    path('wishlist/', WishlistPage.as_view(), name='wishlistpage'),
    path('checkout/', CheckoutPage.as_view(), name='checkoutpage'),
    path('placeorder/', PlaceOrder.as_view(), name='placeorderpage'),
    path('placeorder/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('faqs/', Faqs.as_view(), name='faqpage'),
    path('aboutus/', Aboutus.as_view(), name='aboutuspage'),
    path('help/', Help.as_view(), name='helppage'),
    path('terms/', Terms.as_view(), name='termspage'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
