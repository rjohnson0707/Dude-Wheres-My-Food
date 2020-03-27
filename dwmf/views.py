from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Truck, User, Profile, Menu, Calendar, ProfilePhoto, TruckPhoto, Review
from .forms import ExtendedUserCreationForm, ProfileForm, MenuForm, CalendarForm, EditUser, ReviewForm, MenuUpdate, TruckUpdate
from datetime import date, time, timezone, datetime
from django.db.models import Avg
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

class TruckUpdate(LoginRequiredMixin, UpdateView):
    model = Truck
    fields = ['name', 'style']

class TruckDelete(LoginRequiredMixin, DeleteView):
    model = Truck
    success_url = '/trucks/'
##########################view definitions here

@login_required
def truck_detail(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    calendar_form = CalendarForm()
    a = Review.objects.filter(truck_id=truck_id)
    sum = 0
    avg = 0

    if len(a) > 0:
        for rating in a:
            sum += rating.rating
            avg = sum / len(a)
  
    return render(request, 'dwmf/truck_detail.html', {
        'truck': truck,
        'calendar_form': calendar_form,
        'avg':avg
        })

@login_required
def menu_create(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    menu_form = MenuForm()

    return render(request, 'dwmf/menu_form.html',{'truck':truck, 'menu_form': menu_form})

@login_required
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

@login_required
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
        profile = request.user.profile
    trucks = Truck.objects.all()
    trucks_user_doesnt_favorite = Truck.objects.exclude(id__in = profile.trucks.all().values_list('id'))
    truck = trucks.first()
    return render(request, 'registration/profile.html', {'user': user, 'trucks': trucks, 'trucks_user_doesnt_favorite': trucks_user_doesnt_favorite})

@login_required
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

@login_required
def delete_photo(request, user_id):
    key = ProfilePhoto.objects.get(user_id=user_id)
    key.delete()
    
    return redirect(reverse('profile'))

@login_required
def delete_truck_photo(request, truck_id):
    key = TruckPhoto.objects.get(truck_id=truck_id)
    key.delete()
    
    return redirect('truck_detail', truck_id=truck_id) 

@login_required
def truck_photo(request, truck_id):

    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = TruckPhoto(url=url, truck_id=truck_id)
            photo.save()
        except:
            print('An error occurred uploading the file to the cloud')
    return redirect('truck_detail', truck_id=truck_id)

@login_required
def assoc_truck(request, user_id, truck_id):
    Profile.objects.get(user_id=user_id).trucks.add(truck_id)
    return redirect(reverse('profile'))

@login_required
def unassoc_truck(request, user_id, tk_id):
    Profile.objects.get(user_id=user_id).trucks.remove(tk_id)
    return redirect(reverse('profile'))

def trucks_index(request):
    trucks = Truck.objects.all()
    t = trucks.first()
    print(t.reviews.all())
    return render(request, 'trucks/index.html', {'trucks': trucks })

def trucks_info(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    review_form = ReviewForm()
    a = Review.objects.filter(truck_id=truck_id)
    sum = 0
    if len(a) > 0:
        for rating in a:
            sum += rating.rating
        avg = sum / len(a)   
    else: 
        avg = 'None: Be the first to review!'
    return render(request, 'trucks/index_detail.html', {'truck': truck, 'review_form': review_form, 'avg': avg})

@login_required
def add_review(request, truck_id):
    form = ReviewForm(request.POST)
    user = request.user
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.truck_id = truck_id
        new_review.user_id = user.id
        new_review.created_date = datetime.now()
        new_review.save()
    return redirect('index_detail', truck_id=truck_id)

@login_required
def truck_reviews(request, truck_id):
    reviews = Review.objects.filter(truck=truck_id)
    truck = Truck.objects.get(id=truck_id)
    return render(request, 'dwmf/truck_reviews.html', {'reviews':reviews, 'truck': truck})

@login_required
def delete_review(request, truck_id, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('index_detail', truck_id=truck_id)
    else:
        return render(request, 'trucks/index_detail.html', truck_id=truck_id)

@login_required
def add_calendar(request, truck_id):
   
    form = CalendarForm(request.POST)

    if form.is_valid():

        new_calendar = form.save(commit=False)
        new_calendar.truck_id = truck_id
        new_calendar.save()
    return redirect('truck_detail', truck_id=truck_id)

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = EditUser(request.POST, instance=request.user)
        

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditUser(instance=request.user)
        return render(request, 'registration/edit_user.html', {'form': form}) 

@login_required
def menu_update(request, item_id, truck_id):
    item = Menu.objects.get(id=item_id)
    if request.method == 'POST':
        form = MenuUpdate(request.POST, instance=item)

        if form.is_valid():
            update_item = form.save(commit=False)
            update_item.truck_id = truck_id
            update_item.save()
            return redirect('truck_detail', truck_id=truck_id)
    else:
        form = MenuUpdate(instance=item)
        return render(request, 'dwmf/menu_update.html',{'form': form})

@login_required
def delete_item(request, item_id, truck_id):
    obj = Menu.objects.get(id=item_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('truck_detail', truck_id=truck_id)
    context ={
        truck_id: truck_id,
    }
    return render(request, 'dwmf/truck_detail.html', {'truck_id': truck_id})

@login_required
def delete_calendar(request, calendar_id, truck_id):
    obj = Calendar.objects.get(id=calendar_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('truck_detail', truck_id=truck_id)
    context ={
        truck_id: truck_id,
    }
    return render(request, 'dwmf/truck_detail.html', {'truck_id': truck_id})
