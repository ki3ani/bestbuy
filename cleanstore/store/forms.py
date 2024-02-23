from django import forms
from .models import Order
from allauth.account.forms import SignupForm
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'quantity']  # Include the necessary fields


class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(max_length=15, required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.customer.phone_number = self.cleaned_data['phone_number']
        user.customer.save()
        return user


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15)