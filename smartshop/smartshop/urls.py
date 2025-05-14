from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('autocomplete/', include('search.urls')),  # Autocomplete endpoint
    path('search/', include('search.urls')),  # Search results endpoint
    path('', lambda request: redirect('login')),  # Redirect root URL to the login page
    path('orders/', include('orders.urls')),
]