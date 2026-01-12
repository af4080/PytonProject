from django.utils import timezone

from django import forms

from django import forms
from .models import Task, Team, Profile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password','team','role')

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','min': timezone.now().date()})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date','assigned_to']

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)

        if team:
            self.fields['assigned_to'].queryset = User.objects.filter(
                profile__team=team,
                profile__role='worker'
            )