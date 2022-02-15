from django.urls import path
from .views import StorePage, ProductDetailPage

urlpatterns = [
    path('', StorePage, name='storepage'),
    path('product-detail', ProductDetailPage, name='productdetailpage')
]