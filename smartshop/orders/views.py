from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from products.models import Product

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from products.models import Product

def place_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        address = request.POST.get('address')

        # Debugging: Print the product_id to the console
        print(f"Received product_id: {product_id}")

        if not product_id:
            messages.error(request, "Invalid product selected.")
            return redirect('search_results')

        if not address:
            messages.error(request, "Address is required.")
            return redirect('search_results')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('search_results')

        # Create the order
        order = Order.objects.create(user=request.user, product=product, address=address, status='Placed')
        messages.success(request, "Order placed successfully!")
        return redirect('orders')

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/orders.html', {'orders': user_orders})