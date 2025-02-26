from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .filters import OrderFilter
from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer, OrderItemsSerializer
from rest_framework.pagination import PageNumberPagination

import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse



# ✅ GET ALL ORDERS (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    filterset = OrderFilter(request.GET,queryset=Order.objects.all().order_by('id'))
    count = filterset.qs.count()

    #pagination
    resPerPage = 1
    paginator =PageNumberPagination()
    paginator.page_size= resPerPage
    queryset = paginator.paginate_queryset(filterset.qs,request)



    serialzer = OrderSerializer(queryset,many=True)
    return Response({
        "count":count,
        "resPerPage":resPerPage,
        'orders':serialzer.data})








# ✅ GET INDIVIDUAL ORDERS (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_individual(request,pk):
    order_details = get_object_or_404(Order,pk=pk)
    serialzer = OrderSerializer(order_details,many=False)
    return Response({'order_details':serialzer.data})




# ✅ CREATE ORDER (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    data = request.data  # Get request data
    user = request.user  # Get logged-in user

    # Check if order items exist in request
    order_items = data.get('orderitems', [])
    if not order_items:
        return Response({"error": "No order items provided"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Create order object
    order = Order.objects.create(
        user=user,
        street=data['street'],
        city=data['city'],
        zip_code=data['zip_code'],
        phone_no=data['phone_no'],
        country=data['country'],
        payment_status=data.get('payment_status', 'UNPAID'),
        order_status=data.get('order_status', 'Processing'),
        payment_mode=data.get('payment_mode', 'COD'),
        total_amount=0  # Will be updated after calculating total
    )

    total_amount = 0  # Initialize total amount

    # ✅ Create order items
    for item in order_items:
        product = get_object_or_404(Product, id=item['product'])  # Get product
        if item['quantity'] > product.srock:
            return Response(
                {"error": f"Not enough srock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST
            )

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            name=product.name,
            quantity=item['quantity'],
            price=product.price
        )

        total_amount += item['quantity'] * product.price  # Calculate total price

    # ✅ Update total amount in order
    order.total_amount = total_amount
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# ✅ UPDATE STOCK WHEN ORDER IS SHIPPED
@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_order_status(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    data = request.data

    # Check if status is changing to "Shipped"
    if data.get('order_status') == "Shipped":
        order_items = order.orderitems.all()  # Get all items in order
        for item in order_items:
            if item.product.srock >= item.quantity:
                item.product.srock -= item.quantity  # Deduct stock
                item.product.save()
            else:
                return Response(
                    {"error": f"Not enough srock for {item.product.name}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

    # ✅ Update order status
    order.order_status = data.get('order_status', order.order_status)
    order.save()
    return Response({"detail": f"Order status updated to {order.order_status}"})


  # ✅ Delete order 

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.user != order.user:
        return Response({"error": "You are not authorized to delete this order"}, status=403)
    
    order.delete()
    return Response({"message": "Order deleted successfully"}, status=200)








def sslcommerz_payment(request):
    sslcz_store_id = settings.SSLCOMMERZ["STORE_ID"]
    sslcz_store_pass = settings.SSLCOMMERZ["STORE_PASS"]
    is_sandbox = settings.SSLCOMMERZ["IS_SANDBOX"]

    base_url = "https://sandbox.sslcommerz.com" if is_sandbox else "https://securepay.sslcommerz.com"
    init_url = f"{base_url}/gwprocess/v3/api.php"

    # Define payment data
    payment_data = {
        "store_id": sslcz_store_id,
        "store_passwd": sslcz_store_pass,
        "total_amount": 100.00,  # Change this dynamically
        "currency": "BDT",
        "tran_id": "TEST12345",  # Generate a unique transaction ID
        "success_url": "http://127.0.0.1:8000/payment-success/",
        "fail_url": "http://127.0.0.1:8000/payment-fail/",
        "cancel_url": "http://127.0.0.1:8000/payment-cancel/",
        "cus_name": "John Doe",
        "cus_email": "johndoe@example.com",
        "cus_phone": "01711111111",
        "cus_add1": "Dhaka",
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "product_name": "Test Product",
        "product_category": "General",
        "product_profile": "general"
    }

    # Send request to SSLCOMMERZ
    response = requests.post(init_url, data=payment_data)
    response_data = response.json()

    if response_data.get("status") == "SUCCESS":
        return redirect(response_data["GatewayPageURL"])  # Redirect to SSLCommerz payment page
    else:
        return JsonResponse({"error": "Payment initialization failed"}, status=400)

def payment_success(request):
    return JsonResponse({"message": "Payment Successful!"})
def payment_fail(request):
    return JsonResponse({"message": "Payment Failed!"})
def payment_cancel(request):
    return JsonResponse({"message": "Payment Cancelled!"})
