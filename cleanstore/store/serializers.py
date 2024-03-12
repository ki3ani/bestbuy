from rest_framework import serializers
from .models import Customer, Item, Order, userProfile

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'in_stock']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'customer_number']

class OrderSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for the item field
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    
    class Meta:
        model = Order
        fields = ['id', 'item', 'quantity', 'time']

    def create(self, validated_data):
        # Assume that the request user's customer profile is set in the view.
        # You can access the request in the serializer context as self.context['request'].
        request = self.context['request']
        customer = Customer.objects.get(user=request.user)
        validated_data['customer'] = customer
        return super().create(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['id', 'user', 'phone_number']