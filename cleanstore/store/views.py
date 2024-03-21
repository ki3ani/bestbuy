from django.shortcuts import get_object_or_404, redirect, render
import phonenumbers
from .forms import PhoneNumberForm
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Customer, Item, Order
from .serializers import ItemSerializer, OrderSerializer
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


class HomeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has a phone number
            if not request.user.customer.phone_number:
                # If the phone number is not present, set a session variable
                # to indicate the need for a phone number
                request.session['require_phone_number'] = True
                return redirect('add_phone_number')  # Redirect to the phone number addition page
            
            # Proceed with the normal flow of the view
            items = Item.objects.filter(in_stock=True)
            serializer = ItemSerializer(items, many=True)
            response_data = {
                "message": "Browse and make your orders!",
                "items": serializer.data
            }
            return Response(response_data)
        else:
            # Return the message for unauthenticated users
            message = "You can view items, but you'll need to sign up or register to start making orders."
            response_data = {"message": message}
            return Response(response_data)

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]  # Allow access to authenticated users only

    def list(self, request):
        # Query orders for the logged-in user
        orders = Order.objects.filter(customer=request.user.customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

 

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'in_stock', 'category__name']  # Now you can filter by category name too
    search_fields = ['name', 'description', 'category__name']
    pagination_class = StandardResultsSetPagination


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user.customer)

    def create(self, request, *args, **kwargs):
        # Custom logic for creation, ensuring admins cannot create orders
        if request.user.is_staff:
            return Response({"error": "Admins cannot make orders for customers."}, status=status.HTTP_403_FORBIDDEN)
        # Proceed with the normal creation process
        return super().create(request, *args, **kwargs)



def add_phone_number(request):
    user = request.user

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

                    if not isinstance(user, AnonymousUser):
                        customer = Customer.objects.get(user=user)
                        customer.phone_number = phone_number
                        customer.save()

                        if 'require_phone_number' in request.session:
                            del request.session['require_phone_number']
                        
                        return redirect('home')  # Assuming 'home' is the name of your home page's URL pattern

            except phonenumbers.NumberParseException:
                form.add_error('phone_number', 'This is not a valid phone number.')
    else:
        form = PhoneNumberForm()

    # Check if the user already has a phone number
    if not isinstance(user, AnonymousUser) and Customer.objects.filter(user=user, phone_number__isnull=False).exists():
        # User has a phone number, redirect to home
        return redirect('home')

    return render(request, 'add_phone_number.html', {'form': form})


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        if not isinstance(user, AnonymousUser):
            customer = Customer.objects.get(user=user)
            # Check if the user has a phone number
            if not customer.phone_number:
                # If the phone number is not present, set a session variable
                # to indicate the need for a phone number
                request.session['require_phone_number'] = True
                return redirect('add_phone_number')  # Redirect to the phone number addition page
            else:
                return Response({"phone_number": customer.phone_number})
        return Response({"phone_number": None})

    def retrieve(self, request, pk=None):
        if not isinstance(request.user, AnonymousUser):
            customer = get_object_or_404(Customer, pk=pk, user=request.user)
            # Check if the user has a phone number
            if not customer.phone_number:
                # If the phone number is not present, set a session variable
                # to indicate the need for a phone number
                request.session['require_phone_number'] = True
                return redirect('add_phone_number')  # Redirect to the phone number addition page
            else:
                return Response({"phone_number": customer.phone_number})
        return Response({"error": "User not authenticated"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        user = request.user
        if not isinstance(user, AnonymousUser):
            customer = Customer.objects.get(user=user)
            phone_number = request.data.get('phone_number')
            if phone_number:
                try:
                    parsed_phone = phonenumbers.parse(phone_number, None)
                    if not phonenumbers.is_valid_number(parsed_phone):
                        return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)
                    customer.phone_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
                    customer.save()
                    return Response({"phone_number": customer.phone_number})
                except phonenumbers.NumberParseException:
                    return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"phone_number": None})