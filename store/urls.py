from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.shop, name = 'shop'),
    path('category/<slug:category_slug>/',views.shop, name = 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail, name = 'product_slug'),
    path('search/',views.search, name = 'search'),
    path('submit_review/<int:product_id>/',views.submit_review, name = 'submit_review'),
]