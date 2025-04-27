from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True)
    # email field is already present in AbstractUser

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)
    
class Profile(models.Model):
    DEPARTMENT_CHOICES = [('Men', 'Men'), ('Women', 'Women')]
    AGE_GROUP_CHOICES = [
        ('18-24', '18-24'), ('25-34', '25-34'), ('35-44', '35-44'),
        ('45-54', '45-54'), ('55+', '55+'),
    ]
    FIT_CHOICES = [
        ('slim', 'Slim Fit'), ('regular', 'Regular Fit'), ('relaxed', 'Relaxed Fit'),
        ('loose', 'Loose Fit'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    mobile_number = models.CharField(max_length=15, blank=True)  # Editable field
    delivery_location = models.TextField(blank=True)
    preferred_department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    height_cm = models.PositiveIntegerField(verbose_name="Height (cm)", blank=True, null=True)
    weight_kg = models.PositiveIntegerField(verbose_name="Weight (kg)", blank=True, null=True)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, blank=True, null=True)
    preferred_fit = models.CharField(max_length=10, choices=FIT_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
# Signal to create Profile when a new CustomUser is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save Profile when CustomUser is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()