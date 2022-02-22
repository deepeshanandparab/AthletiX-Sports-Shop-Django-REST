import re
from django.shortcuts import render, redirect
from store.models import CouponCode, Product, Wishlist
from django.http import HttpResponse, JsonResponse
from .supporting_functions import getWishlist
from django.views import View


class HomePage(View):
    def post(self, request):
        pass

    def get(self, request):
        product_list = Product.objects.all().order_by('-created_at')[0:4]
        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
        else:
            cart = {}
        context = {
            'title':'Home',
            'breadcrum': 'Home',
            'wishlist_products': getWishlist(request),
            'cart_list':cart_list,
            'product_list':product_list
        }
        return render(request, 'index.html', context)  


class CartPage(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        delete = request.POST.get('delete')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if not delete:
                    if remove:
                        if quantity <= 1:
                            cart.pop(product)
                        else:    
                            cart[product] = quantity-1
                    else:
                        cart[product] = quantity+1
                else:
                    cart.pop(product)
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('cartpage')


    def get(self, request):
        coupon_code = request.GET.get('coupon')
        coupon = []
        invalid_coupon = {}
        btn_disabled = False

        if coupon_code != None:
            coupon = CouponCode.objects.filter(code=coupon_code)
            if len(coupon) == 0:
                invalid_coupon = {'message':'Invalid coupon code or already expired coupon.'}

        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
            shipping_charges = 100
            btn_disabled = False
        else:
            cart = {}
            shipping_charges = 0
            btn_disabled = True
        context = {
            'title': 'Cart',
            'cart_list': cart_list,
            'wishlist_products': getWishlist(request),
            'coupon': coupon,
            'invalid_coupon': invalid_coupon,
            'shipping': shipping_charges,
            'btn_disabled':btn_disabled
        }

        return render(request, 'cart.html', context)


class WishlistPage(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        remove_wish = request.POST.get('delete')

        if remove_wish:
            product_id = request.POST.get('product')
            product = Product.objects.get(id=product_id)
            if product.wishlist.filter(id=request.user.id).exists():
                product.wishlist.remove(request.user)
                Wishlist.objects.filter(product_id=product, user_id=request.user).delete()
            return redirect('wishlistpage')

        if cart:
            quantity = cart.get(product)
            if quantity:
                    if remove:
                        if quantity <= 1:
                            cart.pop(product)
                        else:    
                            cart[product] = quantity-1
                    else:
                        cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('wishlistpage')


    def get(self, request):

        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
        else:
            cart = {}

        context = {
            'title': 'Wishlist',
            'wishlist_products': getWishlist(request),
            'cart_list': cart_list
        }
        return render(request, 'wishlist.html', context)

       