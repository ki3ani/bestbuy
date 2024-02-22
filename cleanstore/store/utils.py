import africastalking
import os

# Initialize AfricasTalking SDK
username = os.getenv('AFRICAS_TALKING_USERNAME')  # Replace with your username
apikey = os.getenv('AFRICAS_TALKING_APIKEY')  # Replace with your API Key
africastalking.initialize(username, apikey)
sms = africastalking.SMS

def send_sms_notification(phone_number, message):
    try:
        # Sending the message. The `phone_number` must be in international format.
        response = sms.send(message, [phone_number])
        print(f"SMS sent successfully: {response}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
