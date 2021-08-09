from django import forms
from .models import Interview, Mentoring, Activity

# Create mentoring form with data from Mentoring
class MentoringForm(forms.ModelForm):
    class Meta:
        model = Mentoring
        fields = ('mentor', 'date', 'time')
        widgets = {
            'time': forms.TimeInput(format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(MentoringForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

# Create activity form with data from Activity
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ('project', 'file_activity', 'is_approved')

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

# Create interview form with data from Interview
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ('project',)

    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )
