from rest_framework import serializers
from .models import Customer, Item, Order

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'in_stock']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'customer_number']

class OrderSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(slug_field='name', queryset=Item.objects.all())
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'item', 'quantity', 'time']
