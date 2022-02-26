from traceback import print_tb
from store.models import Product, CouponCode, User
import random, string
import datetime


def getWishlistCount(request):
    wishlist_product_list = Product.objects.all()
    wishlist_products = []

    for product in wishlist_product_list:
        if product.wishlist.filter(id=request.user.id).exists():
            wishlist_products.append(product)
    
    return len(wishlist_products)

def getCartProducts(request):
    cart = request.session.get('cart')
    cart_list = []
    if cart:
        ids = list(request.session.get('cart').keys())
        cart_list = Product.get_products_by_id(ids)
    else:
        cart = {}
    return cart_list


def getWishlist(request):
    wishlist_product_list = Product.objects.all()
    wishlist_products = []

    for product in wishlist_product_list:
        if product.wishlist.filter(id=request.user.id).exists():
            wishlist_products.append(product)
    
    return wishlist_products

def generateRandom():
    date = datetime.datetime.now()
    number = random.randint(1,1000)

    random_number = f'ATX{date.day}{date.month}{date.year}_{date.hour}{date.minute}{date.second}_{number}'
    return random_number

    
