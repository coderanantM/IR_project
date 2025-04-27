from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'mobile_number', 'password1', 'password2')

class MobileResetForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)
    otp = forms.CharField(max_length=6, required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'preferred_department', 'height_cm', 'weight_kg',
            'age_group', 'preferred_fit', 'delivery_location', 'mobile_number'
        ]