import random
import logging
import json
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import MobileResetForm
from .models import PasswordResetOTP, CustomUser
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_POST
from .nlp_utils import extract_preferences_from_text


logger = logging.getLogger(__name__)

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, mobile_number=form.cleaned_data['mobile_number'])  # Create a profile for the new user
            return redirect('login')  # Redirect to login after sign up
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {"form": form})

def password_reset_mobile(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        User = get_user_model()
        try:
            user = User.objects.get(mobile_number=mobile)
            otp = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.create(user=user, otp=otp)
            # Integrate with SMS gateway here
            print(f"Send OTP {otp} to {mobile}")  # For demo/testing
            request.session['reset_mobile_user'] = user.id
            return render(request, 'registration/password_reset_mobile_verify.html', {'mobile': mobile})
        except User.DoesNotExist:
            messages.error(request, "Mobile number not found.")
    return render(request, 'registration/password_reset_mobile.html')

def password_reset_mobile_verify(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        user_id = request.session.get('reset_mobile_user')
        if not user_id:
            messages.error(request, "Session expired. Try again.")
            return redirect('password_reset_mobile')
        user = CustomUser.objects.get(id=user_id)
        otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).order_by('-created_at').first()
        if otp_obj and otp_obj.is_valid():
            request.session['otp_verified_user_id'] = user.id
            logger.debug(f"otp_verified_user_id set for user {user.id}")
            return redirect('password_reset_mobile_set_new_password')
        else:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'registration/password_reset_mobile_verify.html')

def password_reset_mobile_set_new_password(request):
    user_id = request.session.get('otp_verified_user_id')
    if not user_id:
        logger.debug("otp_verified_user_id not found in session.")
        messages.error(request, "Session expired or unauthorized access.")
        return redirect('password_reset_mobile')
    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        # Clear session flag after use
        del request.session['otp_verified_user_id']
        messages.success(request, "Password reset successful. Please login.")
        return redirect('login')
    return render(request, 'registration/password_reset_mobile_set_new_password.html')


def password_reset_options(request):
    return render(request, 'registration/password_reset_options.html')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'registration/edit_profile.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle form submission for updating the profile
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')  # Redirect back to the profile page
    else:
        # Display the profile form with pre-filled data
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'title': 'Your Profile'
    }
    return render(request, 'registration/profile.html', context)


        
@csrf_exempt
@login_required
def process_preference_input(request):
    """API endpoint to process text/voice input and return extracted data."""
    import json
    from .nlp_utils import extract_preferences_from_text

    try:
        body = json.loads(request.body)
        text_input = body.get('text', '')
        if not text_input:
            return JsonResponse({'status': 'error', 'message': 'No text provided'}, status=400)

        # Extract preferences using NLP utility
        extracted_data = extract_preferences_from_text(text_input)

        # Return the actual extracted data!
        return JsonResponse({'status': 'success', 'data': extracted_data})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)
