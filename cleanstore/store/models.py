from django.db import models
from django.contrib.auth.models import User
import uuid
import phonenumbers

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_number = models.UUIDField(default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Adjusted max_length for international numbers

    def save(self, *args, **kwargs):
        if self.phone_number:
            try:
                parsed_phone = phonenumbers.parse(self.phone_number, None)
                if not phonenumbers.is_valid_number(parsed_phone):
                    raise ValueError("Invalid phone number format")
                # Optionally format the number in international format before saving
                self.phone_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='orders', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item_name = self.item.name if self.item else 'No item'
        customer_username = self.customer.user.username if self.customer.user else 'No customer'
        return f"{self.quantity} x {item_name} by {customer_username}"




class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.phone_number:
            try:
                parsed_phone = phonenumbers.parse(self.phone_number, None)
                if not phonenumbers.is_valid_number(parsed_phone):
                    raise ValueError("Invalid phone number format")
                # Optionally format the number in international format before saving
                self.phone_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username