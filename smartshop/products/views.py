from django.shortcuts import render
from fuzzywuzzy import fuzz, process
from products.models import Product, Category
from django.http import JsonResponse

def search_results(request):
    query = request.GET.get('q', '').strip()
    category_name = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    products = Product.objects.all()

    # Fuzzy matching for query
    if query:
        # Get all product names and categories for fuzzy matching
        product_names = Product.objects.values_list('name', flat=True)
        category_names = Category.objects.values_list('name', flat=True)

        # Combine product and category names for fuzzy matching
        all_names = list(product_names) + list(category_names)

        # Find the best matches for the query
        matches = process.extract(query, all_names, limit=20, scorer=fuzz.partial_ratio)

        # Extract matched product names and category names
        matched_product_names = [match[0] for match in matches if match[1] > 60]  # Threshold: 60%
        matched_categories = Category.objects.filter(name__in=matched_product_names)

        # Filter products based on fuzzy matches
        products = products.filter(
            name__in=matched_product_names
        ) | products.filter(category__in=matched_categories)

    # Filter by category
    if category_name:
        category = Category.objects.filter(name=category_name).first()
        if category:
            if hasattr(category, 'subcategories') and category.subcategories.exists():
                products = products.filter(category__in=category.subcategories.all())
            else:
                products = products.filter(category=category)

    # Filter by price range
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

    # Fetch all main categories (parent=None) and their subcategories
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