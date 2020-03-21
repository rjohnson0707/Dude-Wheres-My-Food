from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Truck(models.Model):
    name=models.CharField(max_length=50)
    style = models.CharField(max_length=50)


    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('truck_detail', kwargs={'pk': self.id})