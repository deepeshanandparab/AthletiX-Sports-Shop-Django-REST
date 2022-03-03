from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import RegistrationForm
from .models import Profile
from store.models import Order
import re
from athletixsportsshop.supporting_functions import getCartProducts, getWishlist

def RegisterPage(request):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    atr = '@'

    postdata = request.POST
    first_name = postdata.get('first_name')
    last_name = postdata.get('last_name')
    username = postdata.get('username')
    email = postdata.get('email')
    contact = postdata.get('contact')
    

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'contact': contact
    }

    print('value', value)


    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created sucessfully for {username}. You can login now.')
            return redirect('loginpage')
        elif request.POST['first_name'] == '':
            messages.error(request, 'First name field is empty')
        elif request.POST['last_name'] == '':
            messages.error(request, 'Last name field is empty')
        elif request.POST['contact'] == '':
            messages.error(request, 'Contact field is empty')
        elif len(request.POST['contact']) != 10:
            messages.error(request, 'Enter a valid 10 digit contact number')
        elif request.POST['email'] == '':
            messages.error(request, 'Email field is empty')
        elif atr not in request.POST['email']:
            messages.error(request, 'Email is Invalid')
        elif request.POST['password1'] == '':
            messages.error(request, 'Password field is empty')
        elif request.POST['password1'] != request.POST['password2']:
            messages.error(request, 'Passwords do not match')
    else:
        form = RegistrationForm()
    context = {'form': form, 'title': 'Register', 'value': value}
    return render(request, 'register.html', context)


def LoginPage(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session['username'] = request.POST['username']
            print(request.session['username'])
            auth.login(request, user)
            if user.is_superuser:
                return redirect('homepage')
            else:
                return redirect('homepage')
        else:
            messages.error(request, 'Username or Password is incorrect!')
            return render(request, 'login.html', {'title':'Login'})
    else:
        return render(request, 'login.html', {'title':'Login'})


def LogoutPage(request):
        auth.logout(request)
        return redirect('homepage')



class ProfilePage(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    
    def post(self, request):
        pass


    def get(self, request):
        order_list = Order.objects.filter(user=request.user).order_by('-date')

        context = {
                'title':'Profile',
                'order_list':order_list,
                'profile': True,
                'wishlist_products': getWishlist(request),
                'cart_list': getCartProducts(request)
                }
        return render(request, 'profile.html', context)



class OrdersPage(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    
    def post(self, request):
        pass


    def get(self, request):
        order_list = Order.objects.filter(user=request.user).order_by('-date')
        context = {
                'title':'Orders',
                'order_list':order_list,
                'order': True,
                'wishlist_products': getWishlist(request),
                'cart_list': getCartProducts(request)
                }
        return render(request, 'orders.html', context)
