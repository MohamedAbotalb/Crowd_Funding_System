from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from apps.accounts.models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()

class RegistrationForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placeholder": "Enter First Name"
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placeholder": "Enter First Name"
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placeholder": "Enter Last Name"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "type": "email",
        "placeholder": "Enter Email"
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Enter Password"
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Re-enter Password"
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placeholder": "Enter Phone Number"
    }))
    
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "form-control",
        "type": "file"
    }), required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number', 'profile_picture']
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2 :
            raise ValidationError('First name is too short')        
        return  first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2 :
            raise ValidationError('Last name is too short')
        return  last_name

   