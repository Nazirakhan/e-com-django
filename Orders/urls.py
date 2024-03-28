from django.urls import path
from .import views

urlpatterns = [
    path('place_order/',views.place_order,name="place_order"),
    path('payments/',views.payments,name="payments"),
    path('order_complete/',views.order_complete,name="order_complete"),
    path('order_complete/<int:orderID>/<str:transactionID>/download_invoice/render_pdf_view', views.render_pdf_view, name="render_pdf_view"),
]