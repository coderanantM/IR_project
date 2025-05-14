from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
    path('', views.orders, name='orders'),
]