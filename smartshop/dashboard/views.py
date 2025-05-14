from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recommendation.models import SearchHistory
from products.models import Product, Category
from django.db.models import Count, Q

@login_required
def dashboard(request):
    # Fetch the user's most recent searches
    recent_queries = (
        SearchHistory.objects.filter(user=request.user)
        .order_by('-searched_at')
        .values_list('query', flat=True)[:5]
    )

    # Fetch products based on the most recent searches
    recent_products = Product.objects.filter(
        Q(name__in=recent_queries)
    ).distinct()

    # Recommend products based on the most searched queries
    most_searched_queries = (
        SearchHistory.objects.filter(user=request.user)
        .values('query')
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:5]
    )
    recommended_categories = Category.objects.filter(
        products__name__in=[query['query'] for query in most_searched_queries]
    ).distinct()

    # Separate distinct and slicing for recommended products
    recommended_products_queryset = Product.objects.filter(
        category__in=recommended_categories
    ).exclude(id__in=recent_products.values_list('id', flat=True)).distinct()

    recommended_products = list(recommended_products_queryset[:10])  # Convert to a list after slicing

    context = {
        'recent_products': recent_products,
        'recommended_products': recommended_products,
    }
    return render(request, 'dashboard/dashboard.html', context)