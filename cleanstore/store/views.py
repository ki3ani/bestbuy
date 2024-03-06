from django.shortcuts import redirect, render
import phonenumbers
from .forms import PhoneNumberForm
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Customer, Item, Order
from .serializers import ItemSerializer, OrderSerializer
from rest_framework.exceptions import ValidationError



class HomeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # Allow access to all users

    def list(self, request):
        # Query items to display on the home page
        items = Item.objects.filter(in_stock=True)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]  # Allow access to authenticated users only

    def list(self, request):
        # Query orders for the logged-in user
        orders = Order.objects.filter(customer=request.user.customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

 

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(customer=user.customer)

    def create(self, request, *args, **kwargs):
        # Custom logic for creation, ensuring admins cannot create orders
        if request.user.is_staff:
            return Response({"error": "Admins cannot make orders for customers."}, status=status.HTTP_403_FORBIDDEN)
        # Proceed with the normal creation process
        return super().create(request, *args, **kwargs)


def add_phone_number(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            raw_phone_number = form.cleaned_data['phone_number']
            try:
                parsed_phone_number = phonenumbers.parse(raw_phone_number, None)
                if not phonenumbers.is_valid_number(parsed_phone_number):
                    form.add_error('phone_number', 'This is not a valid phone number.')
                else:
                    phone_number = phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)
                    customer = Customer.objects.get(user=request.user)
                    customer.phone_number = phone_number
                    customer.save()
                    if 'require_phone_number' in request.session:
                        del request.session['require_phone_number']
                    return redirect('home')  # Assuming 'home' is the name of your home page's URL pattern
            except phonenumbers.NumberParseException:
                form.add_error('phone_number', 'This is not a valid phone number.')
    else:
        form = PhoneNumberForm()
    return render(request, 'add_phone_number.html', {'form': form})