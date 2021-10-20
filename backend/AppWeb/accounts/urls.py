from django.urls import include, path
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.views import (password_reset_complete, password_reset_confirm,
                                       password_reset_done, password_reset, login, logout)

from . import api, views, forms

app_name = 'accounts'

password_reset_patterns = [
    path('done/', password_reset_complete, {
        'template_name': 'accounts/password/password_reset_complete.html',
        'extra_context': {
            'title': 'Password reset complete',
        }
    }, name='password_reset_complete'),
    path('reset/done/', password_reset_done, {
        'template_name': 'accounts/password/password_reset_done.html',
        'extra_context': {
            'title': 'Password reset done',
        }
    }, name='password_reset_done'),    
    path('reset/<uidb64>/<token>/', password_reset_confirm, {
        'set_password_form': SetPasswordForm,
        'template_name': 'accounts/password/password_reset_confirm.html',
        'post_reset_redirect': '/accounts/password/done/',
        'extra_context': {
            'title': 'Password reset confirm',
        }
    }, name='password_reset_confirm'),
    path('reset/', password_reset, {
        'password_reset_form': PasswordResetForm,
        'template_name': 'accounts/password/password_reset_form.html',
        'email_template_name': 'accounts/email/email_reset.html',
        'post_reset_redirect': '/accounts/password/reset/done/',
        'extra_context': {
            'title': 'Password Reset',
        }
    }, name='password_reset'),
]

profile_patterns = [
    path('login/', login, {'template_name': 'accounts/login.html', 
        'authentication_form': forms.CustomAuthenticationForm}, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', views.signup, name='signup')
]

urlpatterns = [
    path('', include(profile_patterns)),
    path('password/', include(password_reset_patterns)),
    path('perfil/mentor/<int:user_id>/', views.mentor_profile, name='mentorprofile'),
	path('perfil/mentor/editar/<int:user_id>/', views.update_mentor_profile, name='updatementorprofile'),
    path('perfil/jurado/<int:user_id>/', views.jury_profile, name='juryprofile'),
	path('perfil/jurado/editar/<int:user_id>/', views.update_jury_profile, name='updatejuryprofile'),
    path('perfil/coach/<int:user_id>/', views.coach_profile, name='coachprofile'),
	path('perfil/coach/editar/<int:user_id>/', views.update_coach_profile, name='updatecoachprofile'), 
]
