from django.shortcuts import render, redirect
from django.http import HttpResponse
from Carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime

# Create your views here.

def place_order(request,total=0, quantity = 0):
    current_user = request.user
    # if the cart count is equal to zero, then redirect back to shop page

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')
    
    cgst = 0  # Define cgst with default value
    sgst = 0  # Define sgst with default value
    grand_total = 0  # Define grand_total with default value
    shipping = 0
    tax = 0
    for cart_item in cart_items:
        total = total + (cart_item.product.price * cart_item.quantity)
        quantity = quantity + cart_item.quantity
    cgst = (9 * total)/100
    sgst = (9 * total)/100
    tax = cgst + sgst
    shipping = 50
    if total >= 1500:
        grand_total = total + cgst + sgst
    else:
        grand_total = total + cgst + sgst + shipping
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user           = current_user
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country        = form.cleaned_data['country']
            data.state          = form.cleaned_data['state']
            data.city           = form.cleaned_data['city']
            data.zip_code       = form.cleaned_data['zip_code']
            data.order_note     = form.cleaned_data['order_note']
            data.total          = total
            data.order_total    = grand_total
            data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate ordernumber using yr,month,date and id of order_id
            yr = int(datetime.date.today().strftime("%Y"))
            mn = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))
            d = datetime.date(yr,mn,dt)
            current_date = d.strftime("%Y%m%d") #20240322
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')
    else:
        return redirect('checkout')