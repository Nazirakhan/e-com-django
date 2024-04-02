from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, ProfileUserForm
from .models import Account, ProfileUser
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from Orders.models import Order

# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from Carts.views import _cart_id
from Carts.models import Cart, CartItem
import requests

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone = phone
            user.save()

            # Create a ProfileUser object associated with the new user
            profile_user = ProfileUser.objects.create(user=user)

            #User Activation
            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string("account_verification.html",{
                "user":user,
                "domain":current_site,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()
            # messages.success(request,'Account verification mail has been sent ')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'register.html',context) 


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # getting the product variation by cart_id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from theuser to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    ids = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        ids.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = ids[index]
                            cart_item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print("query -> ",query)
                params = dict(x.split("=") for x in query.split("&"))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return redirect('index')
            
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect("login")
    return render(request,'login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations your account is activated.")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')
    

@login_required(login_url = 'login')
def dashboard(request):
    orders= Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count = orders.count()
    profileuser = ProfileUser.objects.get(user_id=request.user.id)
    context = {
        'order_count':order_count,
        'profileuser':profileuser,
    }
    return render(request, 'dashboard.html',context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #Reset Password Email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string("reset_password_email.html",{
                "user":user,
                "domain":current_site,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,"Password reset mail sent to your email...")
            return redirect('login')
        else:
            messages.error(request, "Account doesn't exist!")
            return redirect('forgotPassword')
    return render(request,'forgotPassword.html')


def resetPassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('resetPassword')
    else:
        messages.error(request,"Reset password activation link expired!")
        return redirect('login')
    # return HttpResponse('Ok')

def resetPassword(request):
    if request.method == "POST":
        password = request.POST['create_password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login')
        else:
            messages.error(request, "PAssword doesn't match")
            return redirect('resetPassword')
    else:
        return render(request,"reset_password.html")
    
@login_required(login_url='login')
def my_orders(request):
    my_orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
       'my_orders':my_orders
    }
    return render(request,"my_orders.html", context)

@login_required(login_url='login')
def edit_profile(request):
    profileuser = get_object_or_404(ProfileUser, user=request.user)
    # profileuser, created = ProfileUser.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileUserForm(request.POST, request.FILES, instance=profileuser)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileUserForm(instance=profileuser)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'profileuser':profileuser,
    }
    return render(request,"edit_profile.html", context)


@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact = request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request, "Password updated successfully")
                return redirect('login')
            else:
                messages.error(request, "Current password doesn't match")
                return redirect('change_password')
        else:
            messages.error(request, "New password doesn't match")
            return redirect('change_password')
    return render(request,"change_password.html")