from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Product
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

import json
from django.template.loader import get_template
from xhtml2pdf import pisa

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
    # store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['paymentmethod'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart to oderproduct model
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
    
    # adding cart variations to orderproduct model
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

    # reduce the quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear cart
    CartItem.objects.filter(user=request.user).delete()

    # send order product email notification
    mail_subject = "Thank you for your order"
    message = render_to_string("order_received_email.html",{
        "user":request.user,
        "order":order,
        "cart_items":cart_items,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()

    # send order number and transactionID back to sendData method using JsonResponse
    data = {
        'orderID':order.order_number,
        'transactionID':payment.payment_id,
    }
    return JsonResponse(data)

    
    # return render(request, 'payments.html')

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
    if total >= 1500:
        grand_total = total + cgst + sgst
    else:
        shipping = 50
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
            data.shipping       = shipping
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

            order = Order.objects.get(user=current_user, order_number=order_number,is_ordered=False)
            context = {
                'order':order,
                'cart_items' : cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'shipping': shipping,
            }
            return render(request,'payments.html',context)
    else:
        return redirect('checkout')
    

def order_complete(request):
    orderID = request.GET.get('orderID')
    transactionID = request.GET.get('transactionID')
    try:
        order = Order.objects.get(order_number=orderID, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id = transactionID)

        product_total = 0
        for product in ordered_products:
            product_total = product_total + (product.product_price * product.quantity)
        
        context = {
            'order':order,
            'ordered_products' : ordered_products,
            'transactionID': payment.payment_id,
            'status': payment.status,
            'payment': payment,
            'product_total': product_total,
        }
        return render(request,'ordercomplete.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('index')
    


def render_pdf_view(request,orderID, transactionID):
    order = Order.objects.get(order_number=orderID,is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    payment = Payment.objects.get(payment_id = transactionID)

    product_total = 0
    for product in ordered_products:
        product_total = product_total + (product.product_price * product.quantity)


    template_path = 'pdfdwnd.html'
    
    context = {
            'order':order,
            'ordered_products' : ordered_products,
            'transactionID': payment.payment_id,
            'status': payment.status,
            'payment': payment,
            'product_total': product_total,
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{order.order_number}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
