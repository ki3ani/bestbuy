from rest_framework import serializers
from .models import Customer, Item, Order, userProfile, Category
import pytz 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'in_stock', 'image', 'category', 'category_id']

    def validate_price(self, value):
        """
        Check that the price is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
    


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'customer_number']



class OrderSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    item_name = serializers.CharField(source='item.name', read_only=True)
    price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2, read_only=True)
    total_cost = serializers.SerializerMethodField(read_only=True)
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'item', 'item_name', 'quantity', 'price', 'total_cost', 'time', 'formatted_time']
        read_only_fields = ['time', 'formatted_time']


    def validate_quantity(self, value):
        """
        Check that the quantity is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        """
        Additional custom validation logic can go here.
        """

        if data['item'].in_stock is False:
            raise serializers.ValidationError("The item is not in stock.")
        return data


    def get_formatted_time(self, obj):
        # Convert to Nairobi timezone before formatting
        nairobi_timezone = pytz.timezone('Africa/Nairobi')
        local_time = obj.time.astimezone(nairobi_timezone)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_total_cost(self, obj):
        return obj.item.price * obj.quantity if obj.item else 0

    def create(self, validated_data):
        request = self.context['request']
        customer = Customer.objects.get(user=request.user)
        validated_data['customer'] = customer
        return super().create(validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['id', 'user', 'phone_number']