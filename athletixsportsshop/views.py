from itertools import product
import re
from django.shortcuts import render, redirect
from store.models import CouponCode, Product, Wishlist
from django.http import HttpResponse, JsonResponse
from .supporting_functions import getWishlist, generateRandom
from django.views import View
from datetime import datetime


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
        request.session['coupon_code'] = coupon_code
        coupon = []
        invalid_coupon = {}
        btn_disabled = False

        if coupon_code != None:
            coupon = CouponCode.objects.filter(code=coupon_code)
            now = datetime.now().strftime('%Y-%m-%d')
            
            if not coupon:
                invalid_coupon = {'message':'Invalid coupon code.','status':'Invalid'}
            elif now >= str(coupon[0].expiring_on):
                CouponCode.objects.filter(code=coupon_code).update(status = 'expired')
                coupon = []
                invalid_coupon = {'message':'Coupon code is expired.','status':'Invalid'}
            elif now < str(coupon[0].starting_from):
                CouponCode.objects.filter(code=coupon_code).update(status = 'inactive')        
                coupon = []
                invalid_coupon = {'message':'Coupon code not active yet.','status':'Invalid'}
            elif coupon[0].redeem_count < 1:
                coupon = []
                invalid_coupon = {'message':'Coupon redeemed by other users.','status':'Invalid'}
            elif coupon[0].redeem_by.filter(id=request.user.id).exists():
                coupon = []
                invalid_coupon = {'message':'Coupon is already used.','status':'Invalid'}
                
        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
            shipping_charges = 200
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


class CheckoutPage(View):
    def post(self, request):
        pass


    def get(self, request):
        btn_disabled = False
        coupon_code = request.session.get('coupon_code')
        coupon = []
        invalid_coupon = {}

        if coupon_code != None:
            coupon = CouponCode.objects.filter(code=coupon_code)
            if len(coupon) == 0:
                invalid_coupon = {'message':'Invalid coupon code or already expired coupon.'}

        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
            shipping_charges = 200
            btn_disabled = False
        else:
            cart = {}
            shipping_charges = 0
            btn_disabled = True

        context = {
            'title': 'Checkout',
            'wishlist_products': getWishlist(request),
            'cart_list': cart_list,
            'shipping': shipping_charges,
            'invalid_coupon': invalid_coupon,
            'btn_disabled': btn_disabled,
            'coupon': coupon,
            'random_number': generateRandom()
        }
        return render(request, 'checkout.html', context)

       