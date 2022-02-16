from multiprocessing import context
from django.shortcuts import redirect, render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product

class StorePage(View):
    def post(self, request):
        pass

    def get(self, request):
        all_products = Product.objects.all()

        #--------------------------Sorting With Parameters---------------------------#
        keyword = request.GET.get('name')
        latest = request.GET.get('latest')
        popularity = request.GET.get('popularity')
        best_rating = request.GET.get('best_rating')
        low_price = request.GET.get('low_price')
        high_price = request.GET.get('high_price')

        #--------------------------Filter By Price------------------------------#
        price_all = request.GET.get('price-all')
        price_50_100 = request.GET.get('price-50-100')
        price_101_1000 = request.GET.get('price-101-1000')
        price_1001_3000 = request.GET.get('price-1001-3000')
        price_3001_6000 = request.GET.get('price-3001-6000')
        price_6001_9000 = request.GET.get('price-6001-9000')
        price_9001_12000 = request.GET.get('price-9001-12000')
        filter_dict = {}

        if keyword != None:
            if latest != None:
                product_list = Product.objects.filter(name__contains=keyword, status=True).order_by('-created_at')
            elif popularity != None:
                product_list = Product.objects.filter(name__contains=keyword, status=True).order_by('-created_at')
            elif best_rating != None:
                product_list = Product.objects.filter(name__contains=keyword, status=True).order_by('-created_at')
            elif low_price != None:
                product_list = Product.objects.filter(name__contains=keyword, status=True).order_by('price')
            elif high_price != None:
                product_list = Product.objects.filter(name__contains=keyword, status=True).order_by('-price')
            elif price_50_100 == 'on':
                product_list = Product.objects.filter(price__gte=50, price__lte=100, status=True).order_by('price')
            elif price_101_1000 == 'on':
                product_list = Product.objects.filter(price__gte=101, price__lte=1000, status=True).order_by('price')
            elif price_1001_3000 == 'on':
                product_list = Product.objects.filter(price__gte=1001, price__lte=3000, status=True).order_by('price')
            elif price_3001_6000 == 'on':
                product_list = Product.objects.filter(price__gte=3001, price__lte=6000, status=True).order_by('price')
            elif price_6001_9000 == 'on':
                product_list = Product.objects.filter(price__gte=6001, price__lte=9000, status=True).order_by('price')
            elif price_9001_12000 == 'on':
                product_list = Product.objects.filter(price__gte=9001, price__lte=12000, status=True).order_by('price')
            else:
                product_list = Product.objects.filter(name__contains=keyword, status=True)
                price_all = 'on'
        else:
            if latest != None:
                product_list = Product.objects.filter(status=True).order_by('-created_at')
            elif popularity != None:
                product_list = Product.objects.filter(status=True).order_by('-created_at')
            elif best_rating != None:
                product_list = Product.objects.filter(status=True).order_by('-created_at')
            elif low_price != None:
                product_list = Product.objects.filter(status=True).order_by('price')
            elif high_price != None:
                product_list = Product.objects.filter(status=True).order_by('-price')
            elif price_50_100 == 'on':
                product_list = Product.objects.filter(price__gte=50, price__lte=100, status=True).order_by('price')
                filter_dict = { 'price_50_100':'on'} 
            elif price_101_1000 == 'on':
                product_list = Product.objects.filter(price__gte=101, price__lte=1000, status=True).order_by('price')
                filter_dict = { 'price_101_1000':'on'} 
            elif price_1001_3000 == 'on':
                product_list = Product.objects.filter(price__gte=1001, price__lte=3000, status=True).order_by('price')
                filter_dict = { 'price_1001_3000':'on'} 
            elif price_3001_6000 == 'on':
                product_list = Product.objects.filter(price__gte=3001, price__lte=6000, status=True).order_by('price')
                filter_dict = { 'price_3001_6000':'on'} 
            elif price_6001_9000 == 'on':
                product_list = Product.objects.filter(price__gte=6001, price__lte=9000, status=True).order_by('price')
                filter_dict = { 'price_6001_9000':'on'} 
            elif price_9001_12000 == 'on':
                product_list = Product.objects.filter(price__gte=9001, price__lte=12000, status=True).order_by('price')
                filter_dict = { 'price_9001_12000':'on'} 
            else:
                product_list = Product.objects.filter(status=True)
                filter_dict = { 'price_all':'on'}

        #---------------------------------------------------------------------#

        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 3 * (response.number - 1) + 1 
        
        context = {
            'title':'Store',
            'all_products': all_products,
            'product_list': response,
            'page_size': 3,
            'page_number': page,
            'first_item_number': first_item_number,
            'search_keyword': keyword,
            'filter_dict': filter_dict
            }
        return render(request, 'store.html', context)


def ProductDetailPage(request, id):
    product = Product.objects.get(id=id)
    context = {
                'title':'Product Detail',
                'product': product
                }
    return render(request, 'product-detail.html', context)

