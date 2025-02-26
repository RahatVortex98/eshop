from .models import Order,OrderItem
from rest_framework import serializers

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemsSerializer(many=True, read_only=True)  # 👈 Nested serializer

    class Meta:
        model = Order
        fields = '__all__'
    def get_order_items(self,obj):
        order_items = obj.orederitems.all()
        serializers =OrderItemsSerializer(order_items,many=True)
        return serializers.data