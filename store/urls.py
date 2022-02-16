from django.urls import path
from .views import StorePage, ProductDetailPage

urlpatterns = [
    path('', StorePage.as_view(), name='storepage'),
    path('product-detail/<id>', ProductDetailPage, name='productdetailpage')
]