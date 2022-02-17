from multiprocessing import context
from django.shortcuts import redirect, render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, ProductType

class StorePage(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

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
        
        return redirect('storepage')

    def get(self, request):
        all_products = Product.objects.all()
        cart = request.session.get('cart')
        
        if not cart:
            request.session['cart'] = {}

        #-----------------------Category-------------------------------#

        products_type_list = []
        product_type = ProductType.objects.all()

        for data in product_type:
            temp_type_list = Product.objects.filter(type=data.type)
            products_type_list.append(temp_type_list)


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

        #--------------------------Filter By Category------------------------------#
        category_all = request.GET.get('category_all')
        category_kashmir_willow_bat = request.GET.get('category_kashmir_willow_bat')
        category_english_willow_bat = request.GET.get('category_english_willow_bat')
        category_leather_ball = request.GET.get('category_leather_ball')
        category_batting_gloves = request.GET.get('category_batting_gloves')
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
            #------------------------------------------------------------
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
            #------------------------------------------------------------
            elif category_kashmir_willow_bat == 'on':
                product_list = Product.objects.filter(type='kashmir_willow_bat', status=True).order_by('price')
                filter_dict = { 'category_kashmir_willow_bat':'on'}
            elif category_english_willow_bat == 'on':
                product_list = Product.objects.filter(type='english_willow_bat', status=True).order_by('price')
                filter_dict = { 'category_english_willow_bat':'on'}
            elif category_leather_ball == 'on':
                product_list = Product.objects.filter(type='kashmir_willow_bat', status=True).order_by('price')
                filter_dict = { 'category_leather_ball':'on'}
            elif category_batting_gloves == 'on':
                product_list = Product.objects.filter(type='batting_gloves', status=True).order_by('price')
                filter_dict = { 'category_batting_gloves':'on'}
            #------------------------------------------------------------    
            else:
                product_list = Product.objects.filter(name__contains=keyword, status=True)
                filter_dict = { 'price_all':'on', 'category_all':'on'}
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
            #------------------------------------------------------------
            elif category_kashmir_willow_bat == 'on':
                product_list = Product.objects.filter(type='kashmir_willow_bat', status=True).order_by('price')
                filter_dict = { 'category_kashmir_willow_bat':'on'}
            elif category_english_willow_bat == 'on':
                product_list = Product.objects.filter(type='english_willow_bat', status=True).order_by('price')
                filter_dict = { 'category_english_willow_bat':'on'}
            elif category_leather_ball == 'on':
                product_list = Product.objects.filter(type='kashmir_willow_bat', status=True).order_by('price')
                filter_dict = { 'category_leather_ball':'on'}
            elif category_batting_gloves == 'on':
                product_list = Product.objects.filter(type='batting_gloves', status=True).order_by('price')
                filter_dict = { 'category_batting_gloves':'on'}
            #------------------------------------------------------------  
            else:
                product_list = Product.objects.filter(status=True)
                filter_dict = { 'price_all':'on', 'category_all':'on'}


        paginator = Paginator(product_list, 15)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 15 * (response.number - 1) + 1 
        
        context = {
            'title':'Store',
            'all_products': all_products,
            'product_list': response,
            'page_size': 15,
            'page_number': page,
            'first_item_number': first_item_number,
            'search_keyword': keyword,
            'filter_dict': filter_dict,
            'products_type_list': products_type_list
            }
        return render(request, 'store.html', context)


def ProductDetailPage(request, id):
    product = Product.objects.get(id=id)
    context = {
                'title':'Product Detail',
                'product': product
                }
    return render(request, 'product-detail.html', context)

