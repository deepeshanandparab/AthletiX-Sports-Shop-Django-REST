from django.urls import path
from .views import StorePage, ProductDetailPage, wishlistProduct, wishlistProductDetail

urlpatterns = [
    path('', StorePage.as_view(), name='storepage'),
    path('product-detail/<id>', ProductDetailPage.as_view(), name='productdetailpage'),
    path('addtowishlist/<id>', wishlistProduct, name='product_wishlist'),
    path('addtowishlistdetail/<id>', wishlistProductDetail, name='product_detail_wishlist')
]