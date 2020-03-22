from django.contrib import admin
from .models import Truck, Profile, Menu, Calendar, UserProfile

# Register your models here.

admin.site.register(Truck)
admin.site.register(UserProfile)

admin.site.register(Profile)
admin.site.register(Menu)
admin.site.register(Calendar)
