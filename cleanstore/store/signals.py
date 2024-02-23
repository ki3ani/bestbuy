import os
import africastalking
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer, Order
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API key and username from environment variables
api_key = os.getenv('AFRICAS_TALKING_APIKEY')
username = os.getenv('AFRICAS_TALKING_USERNAME')

if api_key is None or username is None:
    raise ValueError("Africa's Talking API key or username is not set in the environment variables.")

# Initialize Africa's Talking SDK
africastalking.initialize(username=username, api_key=api_key)
sms = africastalking.SMS

@receiver(post_save, sender=Order)
def send_order_confirmation_sms(sender, instance, created, **kwargs):
    if created:
        message = f"Hello, {instance.customer.user.username}. Your order for {instance.item.name} has been placed successfully."
        phone_number = instance.customer.phone_number  # Make sure this is correctly set in your Customer model
        try:
            response = sms.send(message, [phone_number])
            print(response)
        except Exception as e:
            print(f"SMS sending failed: {e}")

@receiver(post_save, sender=User)
def create_or_update_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    # Ensure customer instance is saved if it exists
    elif hasattr(instance, 'customer'):
        instance.customer.save()
