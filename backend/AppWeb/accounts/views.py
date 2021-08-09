from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from . import forms, utils
from .models import ProfileMentor, ProfileJury, ProfileCoach
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from accounts.models import User
from .forms import AccountFormMentor, AccountFormJury, AccountFormCoach
from common.forms import UserForm

def signup(request):
    """Display and handle the registration form."""
    next = request.POST.get('next')

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        form_profile = forms.ProfileForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            #Set user profile data 
            user_profile_id = user.profile.id           
            user.profile = form_profile.save(commit=False)
            user.profile.id = user_profile_id
            user.profile.save()
            
            # Authenticating 
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            utils.send_welcome_email(request, user)            
            if next:
              return redirect(next)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.SignupForm()
        form_profile = forms.ProfileForm()

    page = {
        'title': _('Signup'),
    }

    context = {
        'form': form,
        'form_profile': form_profile,
        'page': page,
        'next': next,
    }
    return render(request, 'accounts/signup.html', context)

#Show mentor profile
@login_required
def mentor_profile(request, user_id):
	title = 'Perfil mentor'
	user = get_object_or_404(User, pk=user_id)
	profile = ProfileMentor.objects.select_related('user').get(user__id=user_id)
	if request.method == 'GET':
		return render(request, 'accounts/mentor_profile/profile.html', locals())

#Edit a mentor profile
@login_required
def update_mentor_profile(request, user_id):
	title = 'Editar perfil mentor'
	user = get_object_or_404(User, pk=user_id)
	profile_mentor = ProfileMentor.objects.select_related('user').get(user__id=user_id)
	if request.method == 'POST':
		form_profile = AccountFormMentor(request.POST, instance = profile_mentor)
		form_user = UserForm(request.POST, instance = user)
		if form_profile.is_valid() and form_user.is_valid():
			user = form_user.save(commit = False)
			profile_mentor = form_profile.save(commit = False)
			user.save()
			profile_mentor.save()
			return redirect(reverse('tracing:mentorhome'))
	else:
		form_profile = AccountFormMentor(instance = profile_mentor)
		form_user = UserForm(instance = user)
	return render(request, 'accounts/mentor_profile/update_profile.html', locals())

#Show jury profile
@login_required
def jury_profile(request, user_id):
	title = 'Perfil jurado'
	user = get_object_or_404(User, pk=user_id)
	profile = ProfileJury.objects.select_related('user').get(user__id=user_id)
	if request.method == 'GET':
		return render(request, 'accounts/jury_profile/profile.html', locals())

#Edit a jury profile
@login_required
def update_jury_profile(request, user_id):
	title = 'Editar perfil jurado'
	user = get_object_or_404(User, pk=user_id)
	profile_jury = ProfileJury.objects.select_related('user').get(user__id=user_id)
	if request.method == 'POST':
		form_profile = AccountFormJury(request.POST, instance = profile_jury)
		form_user = UserForm(request.POST, instance = user)
		if form_profile.is_valid() and form_user.is_valid():
			user = form_user.save(commit = False)
			profile_jury = form_profile.save(commit = False)
			user.save()
			profile_jury.save()
			return redirect(reverse('tracing:juryhome'))
	else:
		form_profile = AccountFormJury(instance = profile_jury)
		form_user = UserForm(instance = user)
	return render(request, 'accounts/jury_profile/update_profile.html', locals())

#Show coach profile
@login_required
def coach_profile(request, user_id):
	title = 'Perfil coach'
	user = get_object_or_404(User, pk=user_id)
	profile = ProfileCoach.objects.select_related('user').get(user__id=user_id)
	if request.method == 'GET':
		return render(request, 'accounts/coach_profile/profile.html', locals())

#Edit a coach profile
@login_required
def update_coach_profile(request, user_id):
	title = 'Editar perfil coach'
	user = get_object_or_404(User, pk=user_id)
	profile_coach = ProfileCoach.objects.select_related('user').get(user__id=user_id)
	if request.method == 'POST':
		form_profile = AccountFormCoach(request.POST, instance = profile_coach)
		form_user = UserForm(request.POST, instance = user)
		if form_profile.is_valid() and form_user.is_valid():
			user = form_user.save(commit = False)
			profile_coach = form_profile.save(commit = False)
			user.save()
			profile_coach.save()
			return redirect(reverse('tracing:coachhome'))
		else:
			print(form_user.errors)
	else:
		form_profile = AccountFormCoach(instance = profile_coach)
		form_user = UserForm(instance = user)
	return render(request, 'accounts/coach_profile/update_profile.html', locals())

# def message(request, code):
#     if code == 'password_reset':
#         message = _(
#             '<strong>We have sent you an email!</strong> Please, follow the instructions to reset your password.')
#         # messages.add_message(request, messages.INFO, message)
#         return render(request, 'accounts/echo.html', locals())
#         # return redirect(reverse('accounts:password_reset'))
# 
#     if code == 'password_reset_confirm':
#         messages.add_message(request, messages.INFO, _(
#             '<strong>Success!</strong> You have changed your password.'))
#         return redirect(reverse('accounts:login'))
# 
#     if code == 'password_change_done':
#         messages.add_message(request, messages.INFO, _(
#             '<strong>Success!</strong> You have changed your password.'))
#         return redirect(reverse('accounts:password_change'))
# 
#     return redirect(reverse('accounts:profile_edit'))
