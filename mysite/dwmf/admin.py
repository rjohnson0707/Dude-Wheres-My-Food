from django.contrib import admin
from .models import Truck, Profile, Menu, Calendar, Review,ProfilePhoto, TruckPhoto

# Register your models here.

admin.site.register(Truck)
admin.site.register(Profile)
admin.site.register(Menu)
admin.site.register(Calendar)
admin.site.register(Review)
admin.site.register(ProfilePhoto)
admin.site.register(TruckPhoto)
