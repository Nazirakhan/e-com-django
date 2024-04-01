from django.shortcuts import render
from store.models import Product

# Create your views here.
def index(request):
    trendy = Product.objects.order_by('-stock').filter(is_available=True)[:4]
    just_add = Product.objects.filter(is_available=True).order_by('-created_date')[:4]

    context = {
        'trendy' : trendy,
        'just_add':just_add,
    }

    return render(request,'index.html', context)

# def shop(request):
#     products = Product.objects.all()
#     return render(request,'shop.html',{'product':products})

# def detail(request):
#     return render(request,'detail.html')

# def cart(request):
#     return render(request,'cart.html')

# def checkout(request):
#     return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')