from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import math
# Create your models here.


class Location(models.Model):
    #Model representing a location.
    place = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        self.place
        return super().__str__()
   
class Chargingspot(models.Model):
    # Model representing a charging spot.
    name = models.CharField(max_length=50, default=None)
    place = models.ForeignKey(Location, on_delete=models.CASCADE)
    

    
    
class Reservation(models.Model):
    # Model representing a reservation for a charging spot.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    chargingspot = models.ForeignKey(Chargingspot, on_delete=models.SET_NULL, null=True)
    completed=models.BooleanField(default=False)
    class Meta:
        ordering = ['starttime']
   

class FeedbackModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chargingspot = models.ForeignKey(Chargingspot, on_delete=models.CASCADE)
    comment = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.chargingspot.name}"