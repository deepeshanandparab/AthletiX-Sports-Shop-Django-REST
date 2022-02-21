from django.urls import path
from .views import StorePage, ProductDetailPage, wishlistProduct, wishlistProductDetail, \
                    submit_review, wishlistAjax

urlpatterns = [
    path('', StorePage.as_view(), name='storepage'),
    path('product-detail/<id>', ProductDetailPage.as_view(), name='productdetailpage'),
    path('submit_review/<id>', submit_review, name='submit_review'),
    path('addtowishlist/<id>', wishlistProduct, name='product_wishlist'),
    path('addtowishlistdetail/<id>', wishlistProductDetail, name='product_detail_wishlist')
]