from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def save(self, commit=True):
            user = super().save(commit=False)

            user.email = self.cleaned_data('email')

            if commit():
                user.save()
            return user

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields= ('first_name', 'last_name') 