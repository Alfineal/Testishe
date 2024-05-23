from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import Profile
from products.models import *
from django.http import HttpResponseRedirect
from accounts.models import Cart, CartItems
from django.contrib.auth.decorators import login_required

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Аккаунт не найден.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Ваш аккаунт не подтверждён!')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Неверные учётные данные')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def delivery_page(request):
    
    return render(request ,'accounts/delivery.html')




def search_venues(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        venues = Product.objects.filter(product_name__contains=searched)
        return render(request, 'accounts/search_venues.html',{'searched':searched, 'venues':venues})
    else:
        return render(request, 'accounts/search_venues.html',{})


def profile_page(request):
    return render(request ,'accounts/profile.html')

@login_required
def payment_page(request):
    
    return render(request ,'accounts/payment.html')

@login_required
def orders_page(request):
    
    return render(request ,'accounts/orders.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(password) < 7:
            messages.warning(request, 'Пароль должен содержать более 7-ми символов!')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Электронная почта уже принята.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name = last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'На вашу почту было отправлено электронное письмо.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("Вы вышли из пользовательского аккаунта"))
    return redirect('/')
    


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect(request, '/')
    except Exception as e:
        return HttpResponse('Неверный Email токен')


def add_to_cart(request, uid):
    try:
        variant = request.GET.get('variant')
        product = Product.objects.get(uid = uid)
        user = request.user
        cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    except Exception as e:
        messages.warning(request, 'Авторизируйтесь, чтобы совершить заказ!')
        return redirect('/accounts/login/')
        


    cart_item = CartItems.objects.create(cart = cart , product = product , )

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size_variant
        cart_item.save()
        


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart(request):
    cart_obj = Cart.objects.get(is_paid = False, user = request.user)
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists():
            messages.warning(request, 'Такого купона не существует.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, 'Купон уже применён.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Сумма вашего заказа должна быть больше {coupon_obj[0].minimum_amount}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, f'Срок действия купона истёк.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'Купон успешно применён!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    context = {'cart' : cart_obj}
    return render(request, 'accounts/cart.html', context)

def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Купон удалён.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
