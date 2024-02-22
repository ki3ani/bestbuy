from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer
from django.conf import settings
from .models import Order
import africastalking
import os

# Initialize Africa's Talking SDK
africastalking.initialize(os.getenv('AFRICAS_TALKING_USERNAME'), os.getenv('AFRICAS_TALKING_API_KEY'))
sms = africastalking.SMS

@receiver(post_save, sender=Order)
def send_order_confirmation_sms(sender, instance, created, **kwargs):
    if created:
        message = f"Hello, {instance.customer.user.username}. Your order for {instance.item.name} has been placed successfully."
        phone_number = instance.customer.phone_number
        try:
            response = sms.send(message, [phone_number])
            print(response)
        except Exception as e:
            print(f"SMS sending failed: {e}")


@receiver(post_save, sender=User)
def create_or_update_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()
