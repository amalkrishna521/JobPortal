from django import forms
from django.contrib.auth.models import User
from .models import studentuser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = studentuser
        fields = ['mobile', 'image', 'gender']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
