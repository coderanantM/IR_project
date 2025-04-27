from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset_mobile/', views.password_reset_mobile, name='password_reset_mobile'),
    path('password_reset_options/', views.password_reset_options, name='password_reset_options'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset_mobile/', views.password_reset_mobile, name='password_reset_mobile'),
    path('password_reset_mobile_verify/', views.password_reset_mobile_verify, name='password_reset_mobile_verify'),
    path('password_reset_mobile_set_new_password/', views.password_reset_mobile_set_new_password, name='password_reset_mobile_set_new_password'),
    path('edit-profile/', views.edit_profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('api/process-preferences/', views.process_preference_input, name='process_preferences'),


]
