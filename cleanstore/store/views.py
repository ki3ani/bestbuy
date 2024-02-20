from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, Order
from .forms import OrderForm
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Home view: Lists all in-stock items for anyone to view
def home(request):
    items = Item.objects.filter(in_stock=True)
    return render(request, 'home.html', {'items': items})

# Item detail view: Shows details of a single item
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'store/item_detail.html', {'item': item})

# Customer dashboard: Shows a logged-in user's orders and allows order creation
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    orders = request.user.customer.orders.all()
    return render(request, 'store/dashboard.html', {'orders': orders, 'form': form})

# Order detail view: Allows viewing details of a specific order
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

# Order update view: Allows editing an existing order
class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'
    success_url = reverse_lazy('dashboard')

# Order delete view: Allows deleting an existing order
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

@login_required
def create_order(request, item_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer  # Assuming a Customer model related to User
            order.item = Item.objects.get(pk=item_id)  # Set the item based on passed item_id
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    # If GET request or invalid form, redirect to item detail or another appropriate page
    return redirect('item_detail', item_id=item_id)
