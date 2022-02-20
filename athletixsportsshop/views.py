import re
from django.shortcuts import render
from store.models import Product
from django.http import HttpResponse, JsonResponse
from .supporting_functions import getWishlist
from django.views import View


class HomePage(View):
    def post(self, request):
        pass

    def get(self, request):
        product_list = Product.objects.all().order_by('-created_at')[0:4]
        ids = list(request.session.get('cart').keys())
        cart_list = Product.get_products_by_id(ids) 
        context = {
            'title':'Home',
            'breadcrum': 'Home',
            'wishlist_products': getWishlist(request),
            'cart_list':cart_list,
            'product_list':product_list
        }
        return render(request, 'index.html', context)   
