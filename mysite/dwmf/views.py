from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Truck, User, Profile, Menu, Calendar, ProfilePhoto
from .forms import ExtendedUserCreationForm, ProfileForm, MenuForm, CalendarForm, EditProfile
import uuid
import boto3


# S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
# BUCKET = 'dwmf'
S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'catcollector02'



#########################################
def home(request):
    return render(request, 'home.html')

##########################class views
class TruckCreate(LoginRequiredMixin, CreateView):
    model = Truck
    fields= ['name', 'style', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


##########################view definitions here

def truck_detail(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    calendar_form = CalendarForm()
    return render(request, 'dwmf/truck_detail.html', {
        'truck': truck,
        'calendar_form': calendar_form
        })

def menu_create(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    menu_form = MenuForm()

    return render(request, 'dwmf/menu_form.html',{'truck':truck, 'menu_form': menu_form})

def menu_new(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    form = MenuForm(request.POST)

    if form.is_valid():
        new_menu = form.save(commit=False)
        new_menu.truck_id = truck.id
        new_menu.save()
    return redirect('truck_detail', truck_id=truck_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
           
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')
        else:
            error_message = 'Invalid Signup - Please try again'
    form = ExtendedUserCreationForm()
    profile_form = ProfileForm()
    context = {'form': form, 'profile_form': profile_form,'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    trucks = Truck.objects.all()
    return render(request, 'registration/profile.html', {'user': user, 'trucks': trucks})

def profile_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = ProfilePhoto(url=url, user_id=user_id)
            photo.save()
        except:
            print('An error occurred uploading the file to the cloud')
    return redirect(reverse('profile'))


# def assoc_truck(request, user_id, truck_id):
#     UserProfile.objects.get(id=user_id).trucks.add(truck_id)
#     return redirect('profile', user_id=user_id)

def trucks_index(request):
    trucks = Truck.objects.all()
    return render(request, 'trucks/index.html', {'trucks': trucks })

def trucks_info(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    return render(request, 'trucks/index_detail.html', {'truck': truck})

def add_calendar(request, truck_id):
   
    form = CalendarForm(request.POST)

    if form.is_valid():

        new_calendar = form.save(commit=False)
        new_calendar.truck_id = truck_id
        new_calendar.save()
    return redirect('truck_detail', truck_id=truck_id)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfile(instance=request.user)
        return render(request, 'registration/edit_profile.html', {'form': form})
