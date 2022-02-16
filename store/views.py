from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product

class StorePage(View):
    def post(self, request):
        pass

    def get(self, request):
        all_products = Product.objects.all()

        keyword = request.GET.get('name')
        latest = request.GET.get('latest')
        popularity = request.GET.get('popularity')
        best_rating = request.GET.get('best_rating')
        low_price = request.GET.get('low_price')
        high_price = request.GET.get('high_price')

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
            else:
                product_list = Product.objects.filter(name__contains=keyword, status=True)
        else:
            if latest != None:
                product_list = Product.objects.filter(name__contains='', status=True).order_by('-created_at')
            elif popularity != None:
                product_list = Product.objects.filter(name__contains='', status=True).order_by('-created_at')
            elif best_rating != None:
                product_list = Product.objects.filter(name__contains='', status=True).order_by('-created_at')
            elif low_price != None:
                product_list = Product.objects.filter(name__contains='', status=True).order_by('price')
            elif high_price != None:
                product_list = Product.objects.filter(name__contains='', status=True).order_by('-price')
            else:
                product_list = Product.objects.filter(name__contains='', status=True)

        paginator = Paginator(product_list, 3)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 3 * (response.number - 1) + 1 

        price_filter = [0,100, 1000, 2000, 4000, 6000, 8000, 10000]
        
        context = {
            'title':'Store',
            'all_products': all_products,
            'product_list': response,
            'page_size': 3,
            'page_number': page,
            'first_item_number': first_item_number,
            'search_keyword': keyword,
            'price_filter': price_filter
            }
        return render(request, 'store.html', context)


def ProductDetailPage(request, id):
    product = Product.objects.get(id=id)
    context = {
                'title':'Product Detail',
                'product': product
                }
    return render(request, 'product-detail.html', context)
