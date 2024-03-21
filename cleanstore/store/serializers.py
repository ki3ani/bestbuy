from rest_framework import serializers
from .models import Customer, Item, Order, userProfile
import pytz 

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'in_stock']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'customer_number']



class OrderSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'item', 'quantity', 'time', 'formatted_time']
        read_only_fields = ['time', 'formatted_time']

    def get_formatted_time(self, obj):
        # Convert to Nairobi timezone before formatting
        nairobi_timezone = pytz.timezone('Africa/Nairobi')
        local_time = obj.time.astimezone(nairobi_timezone)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def create(self, validated_data):
        request = self.context['request']
        customer = Customer.objects.get(user=request.user)
        validated_data['customer'] = customer
        return super().create(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['id', 'user', 'phone_number']