from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Menu, Calendar

class EditProfile(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            )
    # class Meta:
    #     model = Profile
    #     fields = (
    #         'bio',
    #     )
            
    def save(self, commit=True):
        user = super(EditProfile, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        
        return user





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

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields =['food_name', 'description', 'price']

class CalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = ['date', 'time', 'location']
