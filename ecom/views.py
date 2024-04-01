from django.shortcuts import render
from store.models import Product, ReviewRatings


# Create your views here.
def index(request):
    trendy = Product.objects.order_by('-stock').filter(is_available=True)[:4]
    just_add = Product.objects.filter(is_available=True).order_by('-created_date')[:4]

    for trendy_product in trendy:
        t_reviews = ReviewRatings.objects.filter(product_id=trendy_product.id,status=True)
    
    for just_product in just_add:
        j_reviews = ReviewRatings.objects.filter(product_id=just_product.id,status=True)

    context = {
        'trendy' : trendy,
        'just_add':just_add,
        't_reviews':t_reviews,
        'j_reviews':j_reviews,
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