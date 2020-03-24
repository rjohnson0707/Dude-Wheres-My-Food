from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Menu, Calendar, Review



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


class EditUser(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            )
            
    def save(self, commit=True):
        user = super(EditUser, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        
        return user

class EditProfile(UserChangeForm):

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'bio',
            )
            
    def save(self, commit=True):
        user = super(EditProfile, self).save(commit=False)
        user.profile.first_name = self.cleaned_data['first_name']
        user.profile.last_name = self.cleaned_data['last_name']
        user.profile.bio = self.cleaned_data['bio']

        if commit:
            user.save()
        
        return user


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'created_date')



class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields= ('first_name', 'last_name', 'bio') 

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields =['food_name', 'description', 'price']

class CalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = ['date', 'start_time', 'end_time', 'location']

class MenuUpdate(ModelForm):
    class Meta:
        model = Menu
        fields = ['food_name', 'description', 'price']
       
