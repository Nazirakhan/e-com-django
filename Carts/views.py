from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # to get the product fron product id
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    # return HttpResponse(cart_item.product)
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')



def cart(request,total=0, quantity = 0, cart_items=None):
    cgst = 0  # Define cgst with default value
    sgst = 0  # Define sgst with default value
    grand_total = 0  # Define grand_total with default value
    shipping = 0  # Define shipping with default value
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total = total + (cart_item.product.price * cart_item.quantity)
            quantity = quantity + cart_item.quantity
        cgst = (9 * total)/100
        sgst = (9 * total)/100
        shipping = 50
        if total >= 1500:
            grand_total = total + cgst + sgst
        else:
            grand_total = total + cgst + sgst + shipping

    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'cgst': cgst,
        'sgst': sgst,
        'grand_total': grand_total,
        'shipping': shipping,
    }

    return render(request, 'cart.html', context)
