import re
from django.shortcuts import render, redirect
from store.models import Product
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
        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
        else:
            cart = {}
        context = {
            'title': 'Cart',
            'cart_list': cart_list
        }

        return render(request, 'cart.html', context)
       