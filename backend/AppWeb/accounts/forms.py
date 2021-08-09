from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Profile, ProfileMentor, ProfileJury, ProfileCoach

class SignupForm(forms.ModelForm):
    """Create user form."""

    class Meta:
        """Signup form meta data."""

        model = User
        fields = ('first_name', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        """Set required and widgets for fields."""
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['password'].widget = forms.PasswordInput()        

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

    
    def clean_email(self):
        """Validate if email is already used by other user."""
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_('A user with that email already exists.'))
        return email

    def clean_password(self):
        """Validate password with settings constraints."""
        password = self.cleaned_data.get('password')
        password_validation.validate_password(self.cleaned_data.get('password'), self.instance)
        return password

    def save(self, commit=True):
        """Set email and password for new user."""
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Create profile form."""

    class Meta:
        """profile form meta data."""
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Set required and widgets for fields."""
        super(ProfileForm, self).__init__(*args, **kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )
            

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        """Set required and widgets for fields."""
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

# Form to ProfileMentor
class AccountFormMentor(forms.ModelForm):
    class Meta:
        model = ProfileMentor
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(AccountFormMentor, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update(
        #         {
        #             'class': 'form-control',
        #             'style':'font-size:18px;'
        #         }
        #     )
        
        self.fields['phone_number'].widget.attrs.update({'class':'phone_number form-control', 'style':'font-size:18px;'})
        self.fields['specialty'].widget.attrs.update({'class':'form-control', 'style':'font-size:18px;'})

# Form to ProfileJury
class AccountFormJury(forms.ModelForm):
    class Meta:
        model = ProfileJury
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(AccountFormJury, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'phone_number form-control',
                    'style':'font-size:18px;'
                }
            )

# Form to ProfileCoach
class AccountFormCoach(forms.ModelForm):
    class Meta:
        model = ProfileCoach
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(AccountFormCoach, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'phone_number form-control',
                    'style':'font-size:18px;'
                }
            )