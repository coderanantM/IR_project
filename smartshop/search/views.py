from django.shortcuts import render
from fuzzywuzzy import fuzz, process
from products.models import Product, Category
from django.http import JsonResponse
from django.db.models import Q

def search_results(request):
    query = request.GET.get('q', '').strip()
    category_name = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    products = Product.objects.all()

    # --- CATEGORY MATCHING ---
    matched_category = None
    if query:
        # Fuzzy match against category names first
        category_names = Category.objects.values_list('name', flat=True)
        matches = process.extract(query, category_names, limit=1, scorer=fuzz.partial_ratio)
        if matches and matches[0][1] > 80:
            matched_category = Category.objects.filter(name=matches[0][0]).first()
            if matched_category:
                if matched_category.subcategories.exists():
                    products = products.filter(category__in=matched_category.subcategories.all())
                else:
                    products = products.filter(category=matched_category)
        else:
            # Fuzzy match against product names only
            product_names = Product.objects.values_list('name', flat=True)
            matches = process.extract(query, product_names, limit=20, scorer=fuzz.partial_ratio)
            matched_products = [match[0] for match in matches if match[1] > 70]
            products = products.filter(name__in=matched_products)

    # --- CATEGORY FILTER (from sidebar/category link) ---
    if category_name:
        category = Category.objects.filter(name=category_name).first()
        if category:
            if category.subcategories.exists():
                products = products.filter(category__in=category.subcategories.all())
            else:
                products = products.filter(category=category)

    # --- PRICE FILTER ---
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass

    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'category_name': category_name,
        'min_price': min_price,
        'max_price': max_price,
        'count': products.count()
    }
    return render(request, 'search/search_results.html', context)

def autocomplete(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query:
        product_names = Product.objects.values_list('name', flat=True)
        category_names = Category.objects.values_list('name', flat=True)
        all_names = list(product_names) + list(category_names)
        matches = process.extract(query, all_names, limit=10, scorer=fuzz.partial_ratio)
        suggestions = [match[0] for match in matches if match[1] > 70]
    return JsonResponse({'suggestions': suggestions})
