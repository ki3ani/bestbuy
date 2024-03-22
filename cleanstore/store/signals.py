import os
import africastalking
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_logged_in
from django.core.mail import send_mail
from django.conf import settings
from .models import Customer, Order
from dotenv import load_dotenv
import logging
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Environment Variables Check
api_key = os.getenv('AFRICAS_TALKING_APIKEY')
username = os.getenv('AFRICAS_TALKING_USERNAME')

if not api_key or not username:
    logger.critical("Africa's Talking API key or username is missing in the environment variables.")
else:
    # Initialize Africa's Talking SDK
    africastalking.initialize(username=username, api_key=api_key)
    sms = africastalking.SMS

from django.utils.timezone import localtime

@receiver(post_save, sender=Order)
def send_order_confirmation_sms(sender, instance, created, **kwargs):
    if created and api_key and username:
        customer_username = instance.customer.user.username
        item_name = instance.item.name
        order_id = instance.id
        order_date = localtime(instance.date_created).strftime('%Y-%m-%d %H:%M:%S')  # Assuming `date_created` is a datetime field in your Order model
        total_cost = instance.item.price * instance.quantity if instance.item else 0
        phone_number = instance.customer.phone_number

        # Enhanced message with order details
        message = (f"Hello, {customer_username}! Your order #{order_id} for {item_name} has been successfully received "
                   f"as of {order_date}. Total Cost: {total_cost}. "
                   "We are processing it and will update you with the shipping details soon. Thank you for shopping with us!")

        try:
            response = sms.send(message, [phone_number])
            logger.info(f"Order #{order_id} confirmation SMS sent successfully to {phone_number} (User: {customer_username}). API Response: {response}")
        except Exception as e:
            logger.error(f"Failed to send order #{order_id} confirmation SMS to {phone_number} (User: {customer_username}): {e}", exc_info=True)


@receiver(post_save, sender=Order)
def send_email_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        admin_email = os.getenv('ADMIN_EMAIL_ADDRESS', 'admin@example.com')
        subject = 'New Order Notification'
        message = f'New order #{instance.id} has been placed by {instance.customer.user.username}.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])


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
            # If the phone number is not present, set a session variable
            # to indicate the need for a phone number
            request.session['require_phone_number'] = True
    except Customer.DoesNotExist:
        # Handle cases where the user does not have a related Customer object
        pass