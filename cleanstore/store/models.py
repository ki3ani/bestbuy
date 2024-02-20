from django.db import models
from django.contrib.auth.models import User
import uuid

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

    def __str__(self):
        return self.user.username

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='orders', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} by {self.customer.user.username}"
