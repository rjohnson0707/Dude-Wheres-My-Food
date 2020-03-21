from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('trucks/', views.trucks_index, name='index'),
    path('truck/register/', views.TruckCreate.as_view(), name="truck_register"),
    path('truck/<int:pk>/', views.TruckDetail.as_view(), name='truck_detail'),
]