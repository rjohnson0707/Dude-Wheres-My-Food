from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('trucks/', views.trucks_index, name='index'),
    path('trucks/<int:truck_id>', views.trucks_info, name='index_detail'),
    path('truck/register/', views.TruckCreate.as_view(), name="truck_register"),
    path('truck/<int:pk>/', views.TruckDetail.as_view(), name='truck_detail'),
    
]