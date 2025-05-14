from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=20, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"