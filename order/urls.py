from django.urls import path
from .views import create_order, delete_order, get_order_individual, get_orders, payment_cancel, payment_fail, payment_success, sslcommerz_payment, update_order_status

urlpatterns = [
    path('orders/create/', create_order, name="create_order"),
    path('orders/<int:pk>/update_status/', update_order_status, name="update_order_status"),
    path('orders/', get_orders, name="get_orders"),
    path('orders/<str:pk>/', get_order_individual, name="get_order_individual"),
    path('orders/<str:pk>/delete', delete_order, name="delete_order"),




    path("pay/", sslcommerz_payment, name="sslcommerz_payment"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-fail/", payment_fail, name="payment_fail"),
    path("payment-cancel/", payment_cancel, name="payment_cancel"),
]
