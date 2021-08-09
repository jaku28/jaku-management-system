from django import forms
from .models import New, Project, Event, Call
from accounts.models import Profile
from django.contrib.auth.models import User

# Create new form with data from New
class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = '__all__'
    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(NewForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

# Create new form with data from Call
class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        exclude = ('num_projects','has_projects', 'has_evaluations') 
    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

# Create event form 
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

    def validate_date(self):
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

# Form for Project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'location', 'project_type', 'summary', 'detail_description', 'detail_market_needs', 'members', 'link_video']
        widgets = {
            'summary': forms.Textarea(attrs={'rows':5, 'cols':40}),
            'detail_description': forms.Textarea(attrs={'rows':5, 'cols':40}),
            'detail_market_needs': forms.Textarea(attrs={'rows':5, 'cols':40}),
            'members': forms.Textarea(attrs={'rows':5, 'cols':40}),
        }
    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

class BootstrapStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """Set required and widgets for fields."""
        super(BootstrapStyleForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control', # could add form-control-sm
                }
            )

class AccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',) 

    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                    'style':'font-size:18px;'
                }
            )

class UserForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', ) 

    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                    'required':'true',
                    'pattern': '^((\S+ )*\S+)?$',
                    'title':'No poner espacios en blanco al inicio, al final o seguidos.',
                    'style':'font-size:18px;'
                }
            )
