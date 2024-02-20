from django.shortcuts import render, get_object_or_404
from .models import Product
from Carts.models import CartItem, Cart
from category.models import Category
from Carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def shop(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        # 'product':products
        'product':paged_products,
        'product_count':product_count
    }
    return render(request,'shop.html',context)




def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart':in_cart,
    }
    return render(request,'detail.html', context)

def search(request):
    product_count = 0
    product = Product.objects.none()
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword', '')
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = product.count()
    context={
        'product':product,
        'product_count':product_count,
        'keyword':keyword
    }
    return render(request,'shop.html',context)