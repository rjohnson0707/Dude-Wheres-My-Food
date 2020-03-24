from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Menu, Calendar, Review, Truck



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
            'first_name',
            'last_name',
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


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'created_date')



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
        fields = ['date', 'start_time', 'end_time', 'location']

class MenuUpdate(ModelForm):
    class Meta:
        model = Menu
        fields = ['food_name', 'description', 'price']

class TruckUpdate(ModelForm):
    class Meta:
        model = Truck
        fields = ['name', 'style']

    def save(self, commit=True):
        truck = super(TruckUpdate, self).save(commit=False)
        truck.name = self.cleaned_data['name']
        truck.style = self.cleaned_data['style']
        

        if commit:
            truck.save()
    
        return truck
       
