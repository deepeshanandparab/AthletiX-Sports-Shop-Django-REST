from traceback import print_tb
from store.models import Product


def getWishlistCount(request):
    wishlist_product_list = Product.objects.all()
    wishlist_products = []

    for product in wishlist_product_list:
        if product.wishlist.filter(id=request.user.id).exists():
            wishlist_products.append(product)
    
    return len(wishlist_products)


def getWishlist(request):
    wishlist_product_list = Product.objects.all()
    wishlist_products = []

    for product in wishlist_product_list:
        if product.wishlist.filter(id=request.user.id).exists():
            wishlist_products.append(product)
    
    return wishlist_products

