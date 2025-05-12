from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Category


@login_required
def dashboard(request):
    main_categories = Category.objects.filter(parent=None).prefetch_related('subcategories')
    return render(request, "dashboard/dashboard.html")

