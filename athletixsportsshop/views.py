import re
from django.shortcuts import render
from store.models import Product
from .supporting_functions import getWishlistCount

def HomePage(request):
    context = {'title':'Home', 'wishlist_product_count': getWishlistCount(request)}
    return render(request, 'index.html', context)
