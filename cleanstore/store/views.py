from django.shortcuts import redirect, render
from .forms import PhoneNumberForm
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Customer, Item, Order
from .serializers import ItemSerializer, OrderSerializer


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


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


def add_phone_number(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            customer = Customer.objects.get(user=request.user)
            customer.phone_number = phone_number
            customer.save()
            # Clear the session flag
            if 'require_phone_number' in request.session:
                del request.session['require_phone_number']
            return redirect('home') 
    else:
        form = PhoneNumberForm()
    return render(request, 'add_phone_number.html', {'form': form})