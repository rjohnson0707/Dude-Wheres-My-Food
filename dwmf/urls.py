from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('profile/<int:user_id>/profile_photo/', views.profile_photo, name='profile_photo'),
    path('profile/<int:user_id>/delete_photo/', views.delete_photo, name='delete_photo'),
    path('trucks/<int:truck_id>/add_review/', views.add_review, name='add_review'),
    path('trucks/<int:truck_id>/review/<int:review_id>/delete_review/', views.delete_review, name='delete_review'),
    path('profile/<int:user_id>/assoc_truck/<int:truck_id>/', views.assoc_truck, name='assoc_truck'),
    path('profile/<int:user_id>/unnasoc_truck/<int:tk_id>/', views.unassoc_truck, name='unassoc_truck'),
    path('trucks/', views.trucks_index, name='index'),
    path('trucks/<int:truck_id>', views.trucks_info, name='index_detail'),
    path('truck/register/', views.TruckCreate.as_view(), name="truck_register"),
    path('truck/<int:truck_id>/', views.truck_detail, name='truck_detail'),
    path('truck/<int:truck_id>/create', views.menu_create, name='menu_create'),
    path('truck/<int:pk>/update', views.TruckUpdate.as_view(), name='truck_update'),
    path('truck/<int:truck_id>/reviews', views.truck_reviews, name='truck_reviews'),
    path('truck/<int:pk>/delete/', views.TruckDelete.as_view(), name='truck_delete'),
    path('truck/<int:truck_id>/truck_photo/', views.truck_photo, name='truck_photo'),
    path('truck/<int:truck_id>/delete/', views.delete_truck_photo, name='delete_truck_photo'),
    path('truck/<int:truck_id>/create/menu_new', views.menu_new, name='menu_new'),
    path('truck/<int:truck_id>/add_calendar', views.add_calendar, name='add_calendar'),
    path('truck/<int:truck_id>/calendar/<int:calendar_id>/delete', views.delete_calendar, name='delete_calendar'), 
    path('truck/<int:truck_id>/menu/<int:item_id>/menu_update', views.menu_update, name='menu_update'),
    path('truck/<int:truck_id>/menu/<int:item_id>/delete', views.delete_item, name='delete_item')
]