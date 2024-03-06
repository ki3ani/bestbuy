import os
import africastalking
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_logged_in
from django.shortcuts import redirect
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
        item_name = instance.item.name  # Get the name of the ordered item
        message = f"Hello, {instance.customer.user.username}. Your order for {item_name} has been received."
        phone_number = instance.customer.phone_number  # Ensure the phone number is correctly set in your Customer model
        try:
            response = sms.send(message, [phone_number])
            print(response)
        except Exception as e:
            print(f"SMS sending failed: {e}")

@receiver(post_save, sender=User)
def create_or_update_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    elif hasattr(instance, 'customer'):
        instance.customer.save()

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # Check if the user has a phone number
    try:
        customer = user.customer
        if not customer.phone_number:
            # If the phone number is not present, redirect to the phone number form
            # Use a session variable or a flag to indicate the need for a phone number
            request.session['require_phone_number'] = True
            return redirect('add_phone_number') 
    except Customer.DoesNotExist:
        # Handle cases where the user does not have a related Customer object
        pass
