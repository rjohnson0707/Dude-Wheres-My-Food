from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Truck, User

def home(request):
    return render(request, 'home.html')

##########################class views
class TruckCreate(LoginRequiredMixin, CreateView):
    model = Truck
    fields= ['name', 'style', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TruckDetail(LoginRequiredMixin, DetailView):
    model = Truck
    
# class TruckInfo(DetailView):
#     model = Truck
#     def get(self, request):
#         return render(request, 'trucks_detail.html')

##########################view definitions here
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid Signup - Please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def profile(request):
    user = User
    print(user)
    return render(request, 'registration/profile.html', {'user': user})

def trucks_index(request):
    trucks = Truck.objects.all()
    return render(request, 'trucks/index.html', {'trucks': trucks })

def trucks_info(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    return render(request, 'trucks/index_detail.html', {'truck': truck})




