from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    # Your homepage view logic
    return render(request, 'home.html')


def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    orders = Order.objects.all()
    return render(request, 'store/admin_dashboard.html', {'orders': orders})


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


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order_detail.html'
    context_object_name = 'order'

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'store/order_form.html'
    success_url = reverse_lazy('dashboard')

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'store/order_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

