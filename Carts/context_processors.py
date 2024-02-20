from .views import _cart_id
from .models import CartItem, Cart

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)