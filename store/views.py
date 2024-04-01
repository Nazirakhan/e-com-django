from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRatings, ProductGallery
from Carts.models import CartItem, Cart
from category.models import Category
from Orders.models import OrderProduct
from Carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import ReviewRatingsForm
from django.contrib import messages

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

    for product in products:
        reviews = ReviewRatings.objects.filter(product_id=product.id,status=True)
    
    context = {
        # 'product':products
        'product':paged_products,
        'product_count':product_count,
        'reviews':reviews,
    }
    return render(request,'shop.html',context)




def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    
    # product review
    reviews = ReviewRatings.objects.filter(product_id=single_product.id,status=True)
    review_count = reviews.count()

    # product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product' : single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'review_count':review_count,
        'product_gallery':product_gallery,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRatings.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewRatingsForm(request.POST, instance=review)
            messages.success(request,"Thank you!, your review has been updated successfully.")
            return redirect(url)
        except ReviewRatings.DoesNotExist:
            form = ReviewRatingsForm(request.POST)
            if form.is_valid():
                data = ReviewRatings()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,"Thank you!, your review has been submitted successfully.")
                return redirect(url)
