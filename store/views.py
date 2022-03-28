from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, ProductType, Wishlist, RatingReview
from .forms import ReviewForm
from django.contrib import messages
from athletixsportsshop.supporting_functions import getWishlist

class StorePage(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        delete = request.POST.get('delete')
        cart = request.session.get('cart')
        
        if cart:
            if product in cart:
                quantity = cart[product]['quantity']
                if 'size' in cart[product]:
                    cart[product]['size'] = cart[product]['size']
                    if 'color' in cart[product]:
                        cart[product]['color'] = cart[product]['color']
                elif 'color' in cart[product]:
                        cart[product]['color'] = cart[product]['color']
                elif quantity > 0:
                    if not delete:
                        if remove:
                            if quantity <= 1:
                                cart.pop(product)
                            else:
                                cart[product]['quantity'] = quantity - 1
                        else:
                            cart[product]['quantity'] = quantity + 1
                    else:
                        cart.pop(product)
                else:
                    cart[product] = {'quantity':1,'size':None, 'color': None}
            else:
                cart[product] = {'quantity':1,'size':None, 'color': None}
        else:
            cart = {}
            cart[product] = {'quantity':1,'size':None, 'color': None}
        request.session['cart'] = cart
        print(cart)
        
        return redirect('storepage')

    def get(self, request):
        all_products = Product.objects.all()
        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
        else:
            cart = {}
        
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
        category_tennis_bat = request.GET.get('category_tennis_bat')
        category_leather_ball = request.GET.get('category_leather_ball')
        category_batting_gloves = request.GET.get('category_batting_gloves')
        category_kit_bag_junior = request.GET.get('category_kit_bag_junior')
        category_tshirt = request.GET.get('category_tshirt')
        category_track_pant = request.GET.get('category_track_pant')
        category_cap = request.GET.get('category_cap')
        category_shoes = request.GET.get('category_shoes')
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
            elif category_tennis_bat == 'on':
                product_list = Product.objects.filter(type='tennis_bat', status=True).order_by('price')
                filter_dict = { 'category_tennis_bat':'on'}
            elif category_leather_ball == 'on':
                product_list = Product.objects.filter(type='leather_ball', status=True).order_by('price')
                filter_dict = { 'category_leather_ball':'on'}
            elif category_batting_gloves == 'on':
                product_list = Product.objects.filter(type='batting_gloves', status=True).order_by('price')
                filter_dict = { 'category_batting_gloves':'on'}
            elif category_kit_bag_junior == 'on':
                product_list = Product.objects.filter(type='kit_bag_junior', status=True).order_by('price')
                filter_dict = { 'category_kit_bag_junior':'on'}
            elif category_tshirt == 'on':
                product_list = Product.objects.filter(type='tshirt', status=True).order_by('price')
                filter_dict = { 'category_tshirt':'on'}
            elif category_track_pant == 'on':
                product_list = Product.objects.filter(type='track_pant', status=True).order_by('price')
                filter_dict = { 'category_track_pant':'on'}
            elif category_cap == 'on':
                product_list = Product.objects.filter(type='cap', status=True).order_by('price')
                filter_dict = { 'category_cap':'on'}
            elif category_shoes == 'on':
                product_list = Product.objects.filter(type='shoes', status=True).order_by('price')
                filter_dict = { 'category_shoes':'on'}
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
            elif category_tennis_bat == 'on':
                product_list = Product.objects.filter(type='tennis_bat', status=True).order_by('price')
                filter_dict = { 'category_tennis_bat':'on'}
            elif category_leather_ball == 'on':
                product_list = Product.objects.filter(type='leather_ball', status=True).order_by('price')
                filter_dict = { 'category_leather_ball':'on'}
            elif category_batting_gloves == 'on':
                product_list = Product.objects.filter(type='batting_gloves', status=True).order_by('price')
                filter_dict = { 'category_batting_gloves':'on'}
            elif category_kit_bag_junior == 'on':
                product_list = Product.objects.filter(type='kit_bag_junior', status=True).order_by('price')
                filter_dict = { 'category_kit_bag_junior':'on'}
            elif category_tshirt == 'on':
                product_list = Product.objects.filter(type='tshirt', status=True).order_by('price')
                filter_dict = { 'category_tshirt':'on'}
            elif category_track_pant == 'on':
                product_list = Product.objects.filter(type='track_pant', status=True).order_by('price')
                filter_dict = { 'category_track_pant':'on'}
            elif category_cap == 'on':
                product_list = Product.objects.filter(type='cap', status=True).order_by('price')
                filter_dict = { 'category_cap':'on'}
            elif category_shoes == 'on':
                product_list = Product.objects.filter(type='shoes', status=True).order_by('price')
                filter_dict = { 'category_shoes':'on'}
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

        ratings_list = RatingReview.objects.all()
        
        context = {
            'title':'Store',
            'breadcrum': 'Store',
            'all_products': all_products,
            'product_list': response,
            'page_size': 15,
            'page_number': page,
            'first_item_number': first_item_number,
            'search_keyword': keyword,
            'filter_dict': filter_dict,
            'products_type_list': products_type_list,
            'wishlist_products': getWishlist(request),
            'cart_list':cart_list,
            'ratings_list': ratings_list
            }
        return render(request, 'store.html', context)


class ProductDetailPage(View):
    def post(self, request, id):
        size = request.POST.get('size')
        color = request.POST.get('color')

        product = request.POST.get('product')
        product_type = Product.objects.get(id=product)
        remove = request.POST.get('remove')
        delete = request.POST.get('delete')
        cart = request.session.get('cart')
        
        if cart:
            if product in cart:
                quantity = cart[product]['quantity']
                if size:
                    cart[product]['size'] = size
                    if color:
                        cart[product]['color'] = color
                elif color:
                    cart[product]['color'] = color
                elif quantity > 0:
                    if not delete:
                        if remove:
                            if quantity <= 1:
                                cart.pop(product)
                            else:
                                cart[product]['quantity'] = quantity - 1
                        else:
                            cart[product]['quantity'] = quantity + 1
                    else:
                        cart.pop(product)
                else:
                    cart[product] = {'quantity':1,'size':size, 'color': color}
            else:
                cart[product] = {'quantity':1,'size':size, 'color': color}
        else:
            cart = {}
            cart[product] = {'quantity':1,'size':size, 'color': color}
        request.session['cart'] = cart
        print(cart)
        return redirect('productdetailpage', product)

    def get(self, request, id):
        product_list = Product.objects.all()
        rating_list = RatingReview.objects.filter(product=id)
        overall_rating = overallrating(rating_list)
        product = Product.objects.get(id=id)

        cart = request.session.get('cart')

        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
            if id in cart:
                size = request.session.get('cart')[id]['size']
                color = request.session.get('cart')[id]['color']
            else: 
                size = None
                color = None
        else:
            cart = {}
            size = None
            color = None
            request.session['cart'] = {}

        context = {
                    'title':'Product Detail',
                    'breadcrum': 'Store',
                    'product': product,
                    'product_list': product_list,
                    'wishlist_products': getWishlist(request),
                    'rating_list': rating_list,
                    'overall_rating': overall_rating,
                    'cart_list':cart_list,
                    'size': size,
                    'color': color
                    }
        return render(request, 'product-detail.html', context)


def overallrating(rating_list):
    overall_rating = 0.0
    count = 0
    if len(rating_list) > 0:
        count = len(rating_list)
    else:
        count = 1

    for rating in rating_list:
        overall_rating += rating.rating
    return overall_rating/count


@login_required
def wishlistProduct(request, id):
    product = Product.objects.get(id=id)
    is_wishlist = False
    if product.wishlist.filter(id=request.user.id).exists():
        product.wishlist.remove(request.user)
        Wishlist.objects.filter(product_id=product, user_id=request.user).delete()
        is_wishlist = False
    else:
        product.wishlist.add(request.user)
        Wishlist.objects.create(product_id=product, user_id=request.user)
        is_wishlist = True
    return redirect('storepage')


@login_required
def wishlistProductDetail(request, id):
    product = Product.objects.get(id=id)
    is_wishlist = False
    if product.wishlist.filter(id=request.user.id).exists():
        product.wishlist.remove(request.user)
        Wishlist.objects.filter(product_id=product, user_id=request.user).delete()
        is_wishlist = False
    else:
        product.wishlist.add(request.user)
        Wishlist.objects.create(product_id=product, user_id=request.user)
        is_wishlist = True
    return redirect('productdetailpage', id)


def submit_review(request, id):
    if request.method == 'POST':
        try:
            reviews = RatingReview.objects.get(user__id=request.user.id, product__id=id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect('productdetailpage', id)
        except RatingReview.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = RatingReview()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect('productdetailpage', id)


def wishlistAjax(request, id):
    product = Product.objects.get(id=id)
    is_wishlist = False
    if product.wishlist.filter(id=request.user.id).exists():
        product.wishlist.remove(request.user)
        Wishlist.objects.filter(product_id=product, user_id=request.user).delete()
        is_wishlist = False
    else:
        product.wishlist.add(request.user)
        Wishlist.objects.create(product_id=product, user_id=request.user)
        is_wishlist = True
    return JsonResponse({'status':'Wishlisted'})


