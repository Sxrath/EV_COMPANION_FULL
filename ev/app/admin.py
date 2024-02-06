from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Location)
admin.site.register(models.Chargingspot)
admin.site.register(models.Reservation)
admin.site.register(models.FeedbackModel)