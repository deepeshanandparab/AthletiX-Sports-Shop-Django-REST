from itertools import product
import re
from django.shortcuts import render, redirect
from store.models import CouponCode, Product, Wishlist, Order, RatingReview
from account.models import User, Profile, Address 
from django.http import HttpResponse, JsonResponse
from .supporting_functions import getWishlist, generateRandom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib import auth, messages


class HomePage(View):
    def post(self, request):
        pass

    def get(self, request):
        product_list = Product.objects.all().order_by('-created_at')[0:4]
        trendy_products = Product.objects.all().order_by('-sold_quantity')[0:4]
        cart = request.session.get('cart')
        cart_list = []
        if cart:
            ids = list(request.session.get('cart').keys())
            cart_list = Product.get_products_by_id(ids)
        else:
            cart = {}

        ratings_list = RatingReview.objects.all()
        context = {
            'title':'Home',
            'breadcrum': 'Home',
            'wishlist_products': getWishlist(request),
            'cart_list':cart_list,
            'product_list':product_list,
            'trendy_products': trendy_products,
            'ratings_list': ratings_list
        }
        return render(request, 'index.html', context)  


class CartPage(View):
    def post(self, request):
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
            shipping_charges = 0
            btn_disabled = False
            print('cart', cart)
            print('btn_disabled', btn_disabled)
        else:
            cart = {}
            shipping_charges = 0
            btn_disabled = True
            print('cart', cart)
            print('btn_disabled', btn_disabled)
        context = {
            'title': 'Cart',
            'cart_list': cart_list,
            'wishlist_products': getWishlist(request),
            'coupon': coupon,
            'invalid_coupon': invalid_coupon,
            'shipping': shipping_charges,
            'btn_disabled':btn_disabled,
            'product_options':request.session.get('cart')
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
            if product in cart:
                quantity = cart[product]['quantity']
                if quantity > 0:
                    if remove:
                        if quantity <= 1:
                            cart.pop(product)
                        else:
                            cart[product]['quantity'] = quantity - 1
                    else:
                        cart[product]['quantity'] = quantity + 1
                else:
                    cart[product] = {'quantity':1,'size':None, 'color': None}
            else:
                cart[product] = {'quantity':1,'size':None, 'color': None}
        else:
            cart = {}
            cart[product] = {'quantity':1,'size':None, 'color': None}
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


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


class CheckoutPage(LoginRequiredMixin, View):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        request.session['first_name'] = request.POST.get('order_first_name')
        request.session['last_name'] = request.POST.get('order_last_name')
        request.session['email'] = request.POST.get('order_email')
        request.session['addr1'] = request.POST.get('order_addr1')
        request.session['addr2'] = request.POST.get('order_addr2')
        request.session['pincode'] = request.POST.get('order_pincode')
        request.session['country'] = request.POST.get('order_country')
        request.session['city'] = request.POST.get('order_city')
        request.session['state'] = request.POST.get('order_state')
        request.session['zipcode'] = request.POST.get('order_zipcode')
        request.session['contact'] = request.POST.get('order_contact')
        request.session['terms'] = request.POST.get('order_terms')
        request.session['order_amount'] = request.POST.get('order_amount')

        return redirect('placeorderpage')


    def get(self, request):
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
            shipping_charges = 0
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
            'coupon': coupon
        }
        return render(request, 'checkout.html', context)


class PlaceOrder(LoginRequiredMixin, View):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'


    def post(self, request):
        pass

    def get(self, request):
        username = request.session.get('username')
        coupon_code = request.session.get('coupon_code')
        discount_received = CouponCode.objects.filter(code=coupon_code)
        order_amount = int(request.session.get('order_amount'))
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        email = request.session.get('email')
        addr1 = request.session.get('addr1')
        addr2 = request.session.get('addr2')
        pincode = request.session.get('pincode')
        country = request.session.get('country')
        city = request.session.get('city')
        state = request.session.get('state')
        zipcode = request.session.get('zipcode')
        contact = request.session.get('contact')
        terms = request.session.get('terms')

        customer_data = {
            first_name
        }

        currency = 'INR'
        amount = order_amount*100
        request.session['order_amount'] = amount
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'    


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
            shipping_charges = 0
            btn_disabled = False
        else:
            cart = {}
            shipping_charges = 0
            btn_disabled = True

        context = {
            'title': 'Place Order',
            'wishlist_products': getWishlist(request),
            'cart_list': cart_list,
            'shipping': shipping_charges,
            'invalid_coupon': invalid_coupon,
            'btn_disabled': btn_disabled,
            'coupon': coupon,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'addr1':addr1,
            'addr2':addr2,
            'pincode':pincode,
            'country':country,
            'city':city,
            'state':state,
            'zipcode':zipcode,
            'contact':contact,
            'order_amount': order_amount
        }
        return render(request, 'placeorder.html', context)


@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == 'POST':
            coupon_code = request.session.get('coupon_code')
            discount_received = CouponCode.objects.filter(code=coupon_code)
            cart_discount = 0
            if len(discount_received)>0:
                cart_discount = discount_received[0].discount
            else:
                cart_discount = 0
            cart = request.session.get('cart')
            products = Product.get_products_by_id(list(cart.keys()))

            # first_name = request.session.get('first_name')
            # last_name = request.session.get('last_name')
            # email = request.session.get('email')
            addr1 = request.session.get('addr1')
            addr2 = request.session.get('addr2')
            country = request.session.get('country')
            city = request.session.get('city')
            state = request.session.get('state')
            zipcode = request.session.get('zipcode')
            contact = request.session.get('contact')
            terms = request.session.get('terms')
            
            payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            print('params_dict', params_dict)

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                amount = int(request.session.get('order_amount'))

                profile = Profile.objects.get(user=request.user)
                if profile.contact_number is not None:
                    Profile.objects.filter(user=request.user).update(alt_contact = contact)
                else:
                    Profile.objects.filter(user=request.user).update(contact_number = contact)

                address = Address.objects.filter(user=request.user, title='Primary Address')
                if len(address) > 0:
                    if address[0].addr1 == '':
                        Address.objects.filter(user=request.user).update(
                            title = 'Primary Address',
                            addr1 = addr1,
                            addr2 = addr2,
                            zipcode = zipcode,
                            city = city,
                            state = state,
                            country = country
                            )
                    else:
                        Address.objects.filter(user=request.user).update(
                            title = 'Other Address',
                            addr1 = addr1,
                            addr2 = addr2,
                            zipcode = zipcode,
                            city = city,
                            state = state,
                            country = country
                            )
                else:
                    Address.objects.filter(user=request.user).update(
                            title = 'Primary Address',
                            addr1 = addr1,
                            addr2 = addr2,
                            zipcode = zipcode,
                            city = city,
                            state = state,
                            country = country
                            )

            
                for product in products:
                    print('Quantity', cart.get(str(product.id)))
                    order = Order(
                            order_id = razorpay_order_id,
                            order_amount = amount,
                            product = product,
                            user = request.user,
                            quantity = cart.get(str(product.id)).get('quantity'),
                            price = product.price,
                            coupon_used = coupon_code,
                            discount_received = cart_discount,
                            terms = terms,
                            status = 'paid'
                        )

                    if product in products:
                        product = Product.objects.get(id=product.id)
                        product.sold_quantity = cart.get(str(product.id))
                        stock = product.stock_quantity
                        sold = product.sold_quantity.get('quantity')
                        print('stock', stock , 'sold', sold)
                        if stock > 0 and stock >= sold:
                            product.stock_quantity = stock - sold
                            product.sold_quantity = sold
                        product.save()

                    order.save()

                request.session['cart'] = {}
                request.session['first_name'] = {}
                request.session['last_name'] = {}
                request.session['email'] = {}
                request.session['addr1'] = {}
                request.session['addr2'] = {}
                request.session['pincode'] = {}
                request.session['country'] = {}
                request.session['city'] = {}
                request.session['state'] = {}
                request.session['zipcode'] = {}
                request.session['contact'] = {}
                request.session['terms'] = {}
                request.session['order_amount'] = {}

                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    print('Try block entered')
                    print('order id', razorpay_order_id)                    
                    messages.success(request, f'Order placed successfully')
                    return redirect('orderspage')
                except:
                    print('Order Failed')
                    messages.error(request, f'Failed to place an order')
                    return render(request, 'paymentfail.html')
            else:
                print('Signature Verification Failed')
                messages.error(request, f'Failed to place an order')
                return render(request, 'paymentfail.html')
    else:
        print('No Post request')
        return HttpResponseBadRequest()



class Faqs(View):
    def get(self, request):
        context = {'title': 'FAQs'}
        return render(request, 'faq.html', context)


class Aboutus(View):
    def get(self, request):
        context = {'title': 'About Us'}
        return render(request, 'about_us.html', context)


class Help(View):
    def get(self, request):
        context = {'title': 'Help & Support'}
        return render(request, 'help.html', context)


class Terms(View):
    def get(self, request):
        context = {'title': 'Terms and Conditions'}
        return render(request, 'terms.html', context)