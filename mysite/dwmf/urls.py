from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/profile_photo/', views.profile_photo, name='profile_photo'),
    # path('<int:user_id>/assoc_truck/<int:truck_id>/', views.assoc_truck, name='assoc_truck'),
    path('trucks/', views.trucks_index, name='index'),
    path('trucks/<int:truck_id>', views.trucks_info, name='index_detail'),
    path('truck/register/', views.TruckCreate.as_view(), name="truck_register"),
    path('truck/<int:truck_id>/', views.truck_detail, name='truck_detail'),
    path('truck/<int:truck_id>/create', views.menu_create, name='menu_create'),
    path('truck/<int:truck_id>/create/menu_new', views.menu_new, name='menu_new'),
    path('truck/<int:truck_id>/add_calendar', views.add_calendar, name='add_calendar'),  
]